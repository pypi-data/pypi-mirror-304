import copy
import dataclasses
import logging
import random
import time
import typing
import torch
import torch.utils.data
import irisml.core

from .build_dataloader import build_dataloader
from .build_lr_scheduler import LrSchedulerFactory, LrSchedulerConfig
from .build_optimizer import OptimizerFactory
from .ddp_trainer import DDPTrainer
from .plugin_loader import load_plugin
from .trainer import Trainer

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Train a pytorch model.

    This is a simple training baseline.

    Config:
        num_epochs (int): The number of epochs.
        batch_size (int): Batch size.
        base_lr (float): Base learning rate.
        device ('cpu' or 'cuda'): Device for training.
        lr_scheduler (LrSchedulerConfig): Learning rate scheduler config.
        momentum (float): Momentum parameter for optimizer.
        nesterov (bool): Nesterov momentum for SGD.
        val_check_interval (float): Validate every int(num_epochs * val_check_interval) epochs. Mutually exclusive with val_check_interval_epoch.
        val_check_interval_epoch (int): Validate every N epochs.
        val_batch_size (int): Batch size for validation. If not specified, it uses the same batch size as training.
        weight_decay (float): Weight decay.
        num_processes (int): The number of processes to use. Default: 1.
        num_dataloader_workers (int): The number of workers for dataloader. Default: 4.
        no_weight_decay_param_names (Optional[List[str]]): A regex pattern for parameter names to disable weight_decay
        no_weight_decay_module_class_names (Optional[List[str]]): A regex pattern for module class names to disable weight_decay
        lr_scale_param_names (Optional[List[Tuple[str, float]]]): Learning rate scaling for matched parameters.
        plugins (List[str]): Plugins to use for training. Each plugin can have constant values as arguments. e.g. "clip_max_norm(10)".
        random_seed (Optional[int]): Reset the random seed if requested
        ddp_find_unused_parameters (bool): Find unused parameters for DDP training. Default: False.
    """
    VERSION = '0.5.0'

    @dataclasses.dataclass
    class Config:
        num_epochs: int
        batch_size: int = 1
        base_lr: float = 1e-5
        device: typing.Literal['cpu', 'cuda'] | None = None
        lr_scheduler: LrSchedulerConfig | None = None
        accumulate_grad_batches: int | None = None
        momentum: float = 0
        nesterov: bool = False
        optimizer: typing.Literal['sgd', 'adam', 'amsgrad', 'adamw', 'adamw_amsgrad', 'rmsprop', 'zero_adam', 'zero_amsgrad', 'zero_adamw', 'zero_adamw_amsgrad'] = 'sgd'
        val_check_interval: float | None = None
        val_check_interval_epoch: int | None = None
        val_batch_size: typing.Optional[int] = None
        weight_decay: float = 0
        num_processes: int = 1
        num_dataloader_workers: int = 4
        no_weight_decay_param_names: list[str] | None = None
        no_weight_decay_module_class_names: list[str] | None = None
        lr_scale_param_names: list[tuple[str, float]] | None = None
        plugins: list[str] = dataclasses.field(default_factory=list)
        random_seed: int | None = None
        ddp_find_unused_parameters: bool = False

    @dataclasses.dataclass
    class Inputs:
        model: torch.nn.Module
        train_dataset: torch.utils.data.Dataset
        train_transform: typing.Callable
        val_dataset: torch.utils.data.Dataset | None = None
        val_transform: typing.Callable | None = None
        collate_function: typing.Callable | None = None

    @dataclasses.dataclass
    class Outputs:
        model: torch.nn.Module
        elapsed_time: float = 0

    def execute(self, inputs):
        start_time = time.time()
        model = self.train(inputs)
        return self.Outputs(model, time.time() - start_time)

    def dry_run(self, inputs):
        start_time = time.time()
        model = self.train(inputs, dry_run=True)
        return self.Outputs(model, time.time() - start_time)

    def train(self, inputs, dry_run=False) -> torch.nn.Module:
        if self.config.random_seed:  # Reset the random seed if requested. Note that the IRISML platform also resets the seed at the beginning of each task.
            torch.manual_seed(self.config.random_seed)
            random.seed(self.config.random_seed)
            logger.info(f"Reset the random seed to {self.config.random_seed}")

        plugins = [load_plugin(p, self.context) for p in self.config.plugins]
        if dry_run:
            train_dataloader = val_dataloader = None
        else:
            train_dataloader = build_dataloader(inputs.train_dataset, inputs.train_transform, batch_size=self.config.batch_size, accumulate_grad_batches=self.config.accumulate_grad_batches or 1,
                                                num_processes=self.config.num_processes, num_workers=self.config.num_dataloader_workers, collate_function=inputs.collate_function)
            val_dataloader = inputs.val_dataset and build_dataloader(inputs.val_dataset, inputs.val_transform, batch_size=self.config.val_batch_size or self.config.batch_size,
                                                                     shuffle=False, drop_last=False, collate_function=inputs.collate_function)
        device = self._get_device()
        model = copy.deepcopy(inputs.model) if not dry_run else inputs.model  # Save CPU memory on dry run

        optimizer_factory = OptimizerFactory(self.config.optimizer, self.config.base_lr, self.config.weight_decay, self.config.momentum, self.config.nesterov,
                                             self.config.no_weight_decay_param_names, self.config.no_weight_decay_module_class_names,
                                             self.config.lr_scale_param_names)
        lr_scheduler_factory = LrSchedulerFactory(self.config.lr_scheduler, self.config.num_epochs, (len(train_dataloader) // self.config.num_processes) if train_dataloader else 1)

        val_check_interval = self.config.val_check_interval_epoch if self.config.val_check_interval_epoch else self.config.val_check_interval
        trainer_parameters = {'model': model, 'lr_scheduler_factory': lr_scheduler_factory, 'optimizer_factory': optimizer_factory, 'plugins': plugins,
                              'device': device, 'val_check_interval': val_check_interval, 'accumulate_grad_batches': self.config.accumulate_grad_batches}

        trainer = self.get_trainer(trainer_parameters)

        if not dry_run:
            trainer.train(train_dataloader, val_dataloader, num_epochs=self.config.num_epochs)

        return trainer.model

    def get_trainer(self, parameters):
        """Get a trainer instance. This method may be overridden by a subclass."""
        if self.config.num_processes == 1:
            return Trainer(**parameters)
        else:
            return DDPTrainer(num_processes=self.config.num_processes, find_unused_parameters=self.config.ddp_find_unused_parameters, **parameters)

    def _get_device(self) -> torch.device:
        """Get a torch device based on the configuration. If not specified explicitly, it uses cuda if available."""
        if self.config.device:
            device_name = self.config.device
        else:
            device_name = 'cuda' if torch.cuda.is_available() else 'cpu'
            logger.info(f"Training device is selected automatically: {device_name}. To specify the device manually, please set Config.device.")

        return torch.device(device_name)
