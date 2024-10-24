import logging
import multiprocessing
import os
import queue
import torch
from .ddp_utils import create_distributed_data_parallel_model, spawn_and_wait, recreate_dataloader_with_distributed_sampler
from .trainer import Trainer
from .plugins.ddp import Plugin as DDPPlugin

logger = logging.getLogger(__name__)


class DDPTrainer(Trainer):
    """Train with DistributedDataParallel.

    This class assumes single-node multi-device environment.
    """
    def __init__(self, model, lr_scheduler_factory, optimizer_factory, plugins=None, device=torch.device('cpu'), val_check_interval=None, accumulate_grad_batches=None, num_processes=2,
                 find_unused_parameters=False):
        plugins = plugins or []
        plugins.append(DDPPlugin())
        super().__init__(model, lr_scheduler_factory, optimizer_factory, plugins, device, val_check_interval, accumulate_grad_batches)
        if device.type == 'cuda' and torch.cuda.is_available() and num_processes > torch.cuda.device_count():
            raise RuntimeError(f"Distributed training is used with {num_processes} processes, but there are only {torch.cuda.device_count()} devices.")
        if num_processes == 1:
            raise RuntimeError("At least 2 processes are required for DDP training.")

        if device.type == 'cuda':
            # Crashes the process on errors. This setting has very little performance overhead.
            os.environ['NCCL_ASYNC_ERROR_HANDLING'] = '1'

        logger.info(f"Distributed training with {num_processes} processes.")
        self._num_processes = num_processes
        self._find_unused_parameters = find_unused_parameters

    def train(self, train_dataloader, val_dataloader, num_epochs):
        """Spawn processes and run training on each process.

        To send tensors from a child process, the process must be kept alive until the tensors are loaded on the main process.
        """
        mp_queue = multiprocessing.get_context('spawn').JoinableQueue(1)

        if self.device.type == 'cuda':
            torch.cuda.empty_cache()  # Needs to remove the cache on this process since it is not usable from the new processes.

        context = spawn_and_wait(self._train_on_new_process, args=(train_dataloader, val_dataloader, num_epochs, mp_queue), nprocs=self._num_processes)

        logger.info("At least one of the child processes has completed. Now waiting for the outputs.")

        try:
            state_dict = mp_queue.get(timeout=60)  # If it couldn't get the state_dict in 60 seconds, something wrong must have happend.
            try:
                logger.info(list(state_dict.keys()))
                self.model.load_state_dict(state_dict)
            finally:
                mp_queue.task_done()  # Terminate the child process after loading the state_dict.
        except queue.Empty:
            # If there was an exception, join() will kill all the child processes and raise the exception.
            context.join(1)

            # Kill all remaining processes.
            for process in context.processes:
                if process.is_alive():
                    process.terminate()

            raise RuntimeError("Failed to get a trained model from the child process.")

        context.join()

    def _train_on_new_process(self, process_index, train_dataloader, val_dataloader, num_epochs, mp_queue):
        """Method that runs on a new process.

        This method returns immediately after the training if process_index != 0. If process_index == 0, it will wait for the main process to read the trained state_dict.
        """
        device_id = [process_index] if self._device.type == 'cuda' else None
        if self._device.type == 'cuda':
            self._device = torch.device('cuda', process_index)
            torch.cuda.set_device(process_index)

        backend = 'gloo' if device_id is None else 'nccl'
        logger.info(f"New process started on device {self._device}. backend={backend}, rank={process_index}")
        torch.distributed.init_process_group(backend, rank=process_index, world_size=self._num_processes)
        logger.info(f"Initialized the process group on rank {process_index}.")

        # The model needs to be on the target device. Otherwise, DistributedDataParallel() will stuck.
        self._model.to(self._device)

        self._model = create_distributed_data_parallel_model(self.model, device_id, find_unused_parameters=self._find_unused_parameters)

        distributed_train_dataloader = recreate_dataloader_with_distributed_sampler(train_dataloader)
        distributed_val_dataloader = val_dataloader and recreate_dataloader_with_distributed_sampler(val_dataloader)

        super().train(distributed_train_dataloader, distributed_val_dataloader, num_epochs)

        if process_index == 0:
            # All processes have the same model at this point. Sending it to the main process from the 0th process.
            state_dict = self._model.module.to(torch.device('cpu')).state_dict()
            logger.debug("Sending the state_dict from the process 0")
            mp_queue.put(state_dict)
            mp_queue.join()  # Wait until the state_dict is loaded by the main process.

        logger.info(f"Process {process_index} is completed.")
