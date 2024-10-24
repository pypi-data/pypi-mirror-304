import dataclasses
import itertools
import logging
import math
import multiprocessing
import queue
import typing
import torch.nn
import torch.utils.data
import irisml.core
from irisml.tasks.train.build_dataloader import build_dataloader
from irisml.tasks.train.ddp_utils import spawn_processes, recreate_dataloader_with_new_sampler
from irisml.tasks.train.plugin_list import PluginList
from irisml.tasks.train.plugin_loader import load_plugin


logger = logging.getLogger(__name__)


class Predictor:
    def __init__(self, model, plugins, device=torch.device('cpu')):
        self._model = model
        self._device = device
        self._predictor = getattr(model, 'predictor', None)
        self._plugins = plugins

    @property
    def device(self):
        return self._device

    @torch.no_grad()
    def predict(self, dataloader):
        self._model.to(self.device)

        was_training = self._model.training
        self._model.eval()

        # needed for on_prediction_start
        self.dataloader = dataloader

        results = []
        targets = []
        self._model = self._plugins.on_prediction_start(self, self._model)

        for batch_index, batch in enumerate(dataloader):
            batch = self._plugins.on_prediction_batch_start(self, self._model, batch, batch_index)
            batch_results, batch_targets = self.prediction_step(batch, batch_index)
            results.append(batch_results)
            targets.append(batch_targets)
            self._plugins.on_prediction_batch_end(self, self._model, batch, batch_index)

        self._model = self._plugins.on_prediction_end(self, self._model)

        if was_training:
            self._model.train()

        self._model.to(torch.device('cpu'))
        return self._aggregate_results(results), self._aggregate_results(targets)

    def prediction_step(self, batch, batch_index):
        inputs, targets = batch
        inputs = self._to_device(inputs)
        with self._plugins.forward_context():
            if hasattr(self._model, 'prediction_step'):
                batch_results = self._model.prediction_step(inputs)
            elif self._predictor is not None:
                outputs = self._model(inputs)
                batch_results = self._predictor(outputs)
            else:
                batch_results = self._model(inputs)
        batch_results = self._move_to_cpu(batch_results)
        targets = self._unpin_memory(targets)
        return batch_results, targets

    def _aggregate_results(self, results: typing.List):
        if torch.is_tensor(results[0]):
            if all(results[0].shape[1:] == r.shape[1:] for r in results):
                return torch.cat(results)
            else:
                return list(itertools.chain.from_iterable(list(x) for x in results))
        elif isinstance(results[0], list):
            if isinstance(results[0][0], dict):
                return [d for sublist in results for d in sublist]
            return list(itertools.chain(*results))
        else:
            raise RuntimeError(f"Unexpected result types: {results[0]}")

    def _to_device(self, data):
        if isinstance(data, list):
            return [self._to_device(d) for d in data]
        elif isinstance(data, tuple):
            return tuple(self._to_device(d) for d in data)
        elif hasattr(data, 'to'):
            return data.to(self.device, non_blocking=True)
        return data

    @staticmethod
    def _move_to_cpu(value):
        if torch.is_tensor(value):
            if value.is_pinned():
                return value.detach().clone()
            return value.to(torch.device('cpu'))  # Do not use non_blocking copy here. It'll make a tensor on pinned memory and consume a lot of memory.
        elif isinstance(value, list):
            return [Predictor._move_to_cpu(x) for x in value]
        elif isinstance(value, (int, float, str)):
            return value
        elif isinstance(value, dict):
            return {Predictor._move_to_cpu(k): Predictor._move_to_cpu(v) for k, v in value.items()}
        else:
            raise ValueError(f"Unexpected value type: {type(value)}")

    @staticmethod
    def _unpin_memory(value):
        if torch.is_tensor(value):
            if value.is_pinned():
                return value.detach().clone()
            else:
                return value
        elif isinstance(value, list):
            return [Predictor._unpin_memory(x) for x in value]
        elif isinstance(value, dict):
            return {Predictor._unpin_memory(k): Predictor._unpin_memory(v) for k, v in value.items()}
        elif isinstance(value, (int, float, str)):
            return value
        elif value is None:
            return None
        else:
            raise ValueError(f"Unexpected value type: {type(value)}")


class SubsetSequentialSampler(torch.utils.data.Sampler):
    def __init__(self, data_source, start_index, end_index):
        self._start_index = start_index
        self._end_index = end_index
        assert start_index < end_index
        super().__init__(data_source)

    def __len__(self):
        return self._end_index - self._start_index

    def __iter__(self):
        return iter(range(self._start_index, self._end_index))


class DistributedPredictor(Predictor):
    def __init__(self, model, num_processes, plugins, device=torch.device('cpu')):
        self._num_processes = num_processes
        super().__init__(model, plugins, device)

    def predict(self, dataloader):
        mp_queue = multiprocessing.get_context('spawn').JoinableQueue(self._num_processes)
        num_examples_per_process = math.ceil(len(dataloader.dataset) / self._num_processes)
        context = spawn_processes(self._predict_on_new_process, args=(dataloader, num_examples_per_process, mp_queue), nprocs=self._num_processes)
        all_results = {}

        while len(all_results) < self._num_processes:
            try:
                index, results = mp_queue.get(timeout=5)
                assert index not in all_results
                all_results[index] = results
            except queue.Empty:
                if not all(p.is_alive() for p in context.processes):
                    context.join(1)
                    raise RuntimeError("Failed to collect prediction results from the child processes.")

        aggregated_results = self._aggregate_results([all_results[i][0] for i in range(self._num_processes)])
        aggregated_targets = self._aggregate_results([all_results[i][1] for i in range(self._num_processes)])

        for _ in range(self._num_processes):
            mp_queue.task_done()

        context.join(5)

        return aggregated_results, aggregated_targets

    def _predict_on_new_process(self, process_index, dataloader, num_examples_per_process, mp_queue):
        if self._device.type == 'cuda':
            self._device = torch.device('cuda', process_index)
        start_index = num_examples_per_process * process_index
        end_index = min(len(dataloader.dataset), start_index + num_examples_per_process)
        logger.info(f"Launched a process {process_index} on device {self._device} for batches [{start_index}, {end_index}].")
        sampler = SubsetSequentialSampler(dataloader.dataset, start_index, end_index)
        subset_dataloader = recreate_dataloader_with_new_sampler(dataloader, sampler)
        try:
            results = super().predict(subset_dataloader)
        except Exception as e:
            logger.exception(f"Exception happend while predicting. {e}")
            raise
        logger.info(f"Completed predictions on the process {process_index}. Returning {len(results)} results.")

        mp_queue.put((process_index, results))
        mp_queue.join()


class Task(irisml.core.TaskBase):
    """Predict using a given model.

    This class assumes that the model.predictor returns a Tensor or a list of results.

    Config:
        batch_size (int): The batch size
        device (Optional['cpu' or 'cuda']): The device to run inference
        num_processes (int): The number of processes to use
        plugins (List[str]): List of plugins to use
    """
    VERSION = '0.2.5'

    @dataclasses.dataclass
    class Inputs:
        dataset: torch.utils.data.Dataset
        model: torch.nn.Module
        transform: typing.Optional[typing.Callable] = None
        collate_function: typing.Optional[typing.Callable] = None

    @dataclasses.dataclass
    class Config:
        batch_size: int = 1
        device: typing.Optional[typing.Literal['cpu', 'cuda']] = None
        num_processes: int = 1
        num_dataloader_workers: int = 4
        plugins: typing.List[str] = dataclasses.field(default_factory=list)

    @dataclasses.dataclass
    class Outputs:
        predictions: typing.Union[typing.List, torch.Tensor] = dataclasses.field(default_factory=list)
        targets: typing.Optional[typing.Union[typing.List, torch.Tensor]] = None

    def execute(self, inputs):
        results = self._predict(inputs)
        return self.Outputs(results[0], results[1])

    def _predict(self, inputs):
        plugins = PluginList([load_plugin(p, self.context) for p in self.config.plugins])
        dataloader = build_dataloader(inputs.dataset, inputs.transform, batch_size=self.config.batch_size, num_workers=self.config.num_dataloader_workers,
                                      shuffle=False, drop_last=False, collate_function=inputs.collate_function)
        if self.config.num_processes == 1:
            predictor = Predictor(inputs.model, plugins, self._get_device())
        else:
            predictor = DistributedPredictor(inputs.model, self.config.num_processes, plugins, self._get_device())
        results = predictor.predict(dataloader)
        if len(inputs.dataset) != len(results[0]):
            raise RuntimeError(f"Couldn't get the expected number of prediction results. Expected: {len(inputs.dataset)}. Actual: {len(results[0])}")
        return results

    def _get_device(self) -> torch.device:
        """Get a torch device based on the configuration. If not specified explicitly, it uses cuda if available."""
        if self.config.device:
            device_name = self.config.device
        else:
            device_name = 'cuda' if torch.cuda.is_available() else 'cpu'
            logger.info(f"Training device is selected automatically: {device_name}. To specify the device manually, please set Config.device.")

        return torch.device(device_name)
