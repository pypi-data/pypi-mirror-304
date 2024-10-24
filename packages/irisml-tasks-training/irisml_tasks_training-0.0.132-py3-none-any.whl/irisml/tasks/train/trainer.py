import logging
import torch
from .plugin_list import PluginList

logger = logging.getLogger(__name__)


class Trainer:
    def __init__(self, model, lr_scheduler_factory, optimizer_factory, plugins=None, device=torch.device('cpu'), val_check_interval=None, accumulate_grad_batches=None):
        """Initialize the trainer class.

        Args:
            model (torch.nn.Module): Target model.
            optimizer_factory ((parameters) => torch.optim.Optimizer): A function to instantiate an optimizer.
            val_check_interval (int or float): validate() will be called every N epochs. If val_check_interval is float, N = int(num_epochs * val_check_interval).
        """
        self._model = model
        self._lr_scheduler_factory = lr_scheduler_factory
        self._optimizer_factory = optimizer_factory
        self._optimizer = None
        model_plugins = model.plugins if hasattr(model, 'plugins') else []
        self._plugins = PluginList(model_plugins + (plugins or []))
        self._device = device
        self._val_check_interval = val_check_interval
        self._accumulate_grad_batches = accumulate_grad_batches
        self.criterion = getattr(model, 'criterion', None)
        if not hasattr(self.model, 'training_step') and not self.criterion:
            raise RuntimeError(f"A model must provide training_step() method or a criterion property. model={type(self.model)}")

    @property
    def model(self):
        """Returns a model instance. It is on the target device during a training phase."""
        return self._model

    @property
    def device(self):
        return self._device

    @property
    def optimizer(self):
        """Returns an optimizer instance. Returns None if it's not in training phase."""
        return self._optimizer

    def train(self, train_dataloader, val_dataloader, num_epochs):
        # Saving to instance varialbes so that the plugins can access them.
        self.num_epochs = num_epochs
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader

        self.model.to(self.device)

        self._optimizer = self._optimizer_factory(self.model)
        self._lr_scheduler = self._lr_scheduler_factory(self._optimizer)

        if self.criterion:
            self.criterion.to(self.device)

        val_interval = 0 if not self._val_check_interval else (self._val_check_interval if isinstance(self._val_check_interval, int) else num_epochs * self._val_check_interval)

        self._model = self._plugins.on_train_start(self, self.model)
        for epoch in range(num_epochs):
            self.model.train()
            if not self.train_epoch(train_dataloader, epoch):
                break
            if val_interval and epoch % val_interval == 0:
                self.model.eval()
                self.validate(val_dataloader)

        self._plugins.on_train_end(self, self.model)
        self.model.to(torch.device('cpu'))
        self.model.train()
        self._optimizer = None
        self._lr_scheduler = None

    @torch.no_grad()
    def validate(self, val_dataloader):
        outputs = []
        self._plugins.on_validation_start(self, self.model)
        for batch_index, batch in enumerate(val_dataloader):
            batch = self._plugins.on_validation_batch_start(self, self.model, batch, batch_index)
            loss = self.training_step(batch, batch_index)
            outputs.append(loss)
            self._plugins.on_validation_batch_end(self, self.model, loss, batch, batch_index)

        self._plugins.on_validation_end(self, self.model)
        return outputs

    def train_epoch(self, dataloader, epoch):
        """Train for an epoch.

        Returns: False if the training should be stopped.
        """
        if not self._plugins.on_train_epoch_start(self, self.model, epoch):
            self._plugins.on_train_epoch_end(self, self.model, epoch)
            return False

        # Resetting the gradients at every epoch.
        self._optimizer.zero_grad()

        for batch_index, batch in enumerate(dataloader):
            batch = self._plugins.on_train_batch_start(self, self.model, batch, batch_index)
            loss = self.training_step(batch, batch_index)
            loss = self._plugins.on_train_backward_start(self, self.model, loss)
            if self._accumulate_grad_batches:
                loss /= self._accumulate_grad_batches
            loss.backward()
            self._plugins.on_train_backward_end(self, self.model)

            if not self._accumulate_grad_batches or (batch_index + 1) % self._accumulate_grad_batches == 0:
                # On gradient accumulation, ignore the remainder batches for implementation simplicity.
                optimizer = self._plugins.on_optimizer_step_start(self, self.model, self._optimizer)
                optimizer.step()
                self._optimizer.zero_grad()

            self._plugins.on_train_batch_end(self, self.model, loss, batch, batch_index)
            self._lr_scheduler.step()

        self._plugins.on_train_epoch_end(self, self.model, epoch)
        return True

    def training_step(self, batch, batch_index) -> torch.Tensor:
        inputs, targets = self._to_device(batch)
        with self._plugins.forward_context():
            if hasattr(self.model, 'training_step'):
                loss = self.model.training_step(inputs, targets)['loss']
            else:
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
        return loss

    def _to_device(self, data):
        if isinstance(data, list):
            return [self._to_device(d) for d in data]
        elif isinstance(data, tuple):
            return tuple(self._to_device(d) for d in data)
        elif hasattr(data, 'to'):
            return data.to(self.device, non_blocking=True)
        return data
