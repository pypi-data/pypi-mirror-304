import contextlib


class PluginList:
    """Provides a single Plugin interface for a list of plugins."""
    def __init__(self, plugins):
        self._plugins = plugins

    def on_train_start(self, trainer, model):
        for plugin in self._plugins:
            maybe_model = plugin.on_train_start(trainer, model)
            if maybe_model is not None:
                model = maybe_model
        return model

    def on_train_end(self, trainer, model):
        for plugin in self._plugins:
            maybe_model = plugin.on_train_end(trainer, model)
            if maybe_model is not None:
                model = maybe_model
        return model

    def on_train_epoch_start(self, trainer, model, epoch_index):
        flag = True
        for plugin in self._plugins:
            flag &= plugin.on_train_epoch_start(trainer, model, epoch_index)
        return flag

    def on_train_epoch_end(self, trainer, model, epoch_index):
        for plugin in self._plugins:
            plugin.on_train_epoch_end(trainer, model, epoch_index)

    def on_train_batch_start(self, trainer, model, batch, batch_index):
        for plugin in self._plugins:
            batch = plugin.on_train_batch_start(trainer, model, batch, batch_index)
        return batch

    def on_train_batch_end(self, trainer, model, loss, batch, batch_index):
        for plugin in self._plugins:
            plugin.on_train_batch_end(trainer, model, loss, batch, batch_index)

    def on_train_backward_start(self, trainer, model, loss):
        for plugin in self._plugins:
            loss = plugin.on_train_backward_start(trainer, model, loss)
        return loss

    def on_train_backward_end(self, trainer, model):
        for plugin in self._plugins:
            plugin.on_train_backward_end(trainer, model)

    def on_optimizer_step_start(self, trainer, model, optimizer):
        for plugin in self._plugins:
            optimizer = plugin.on_optimizer_step_start(trainer, model, optimizer)
        return optimizer

    def on_validation_start(self, trainer, model):
        for plugin in self._plugins:
            plugin.on_validation_start(trainer, model)

    def on_validation_end(self, trainer, model):
        for plugin in self._plugins:
            plugin.on_validation_end(trainer, model)

    def on_validation_batch_start(self, trainer, model, batch, batch_index):
        for plugin in self._plugins:
            batch = plugin.on_validation_batch_start(trainer, model, batch, batch_index)
        return batch

    def on_validation_batch_end(self, trainer, model, loss, batch, batch_index):
        for plugin in self._plugins:
            plugin.on_validation_batch_end(trainer, model, loss, batch, batch_index)

    def on_prediction_start(self, trainer, model):
        for plugin in self._plugins:
            maybe_model = plugin.on_prediction_start(trainer, model)
            if maybe_model is not None:
                model = maybe_model
        return model

    def on_prediction_end(self, trainer, model):
        for plugin in self._plugins:
            maybe_model = plugin.on_prediction_end(trainer, model)
            if maybe_model is not None:
                model = maybe_model
        return model

    def on_prediction_batch_start(self, trainer, model, batch, batch_index):
        for plugin in self._plugins:
            batch = plugin.on_prediction_batch_start(trainer, model, batch, batch_index)
        return batch

    def on_prediction_batch_end(self, trainer, model, batch, batch_index):
        for plugin in self._plugins:
            plugin.on_prediction_batch_end(trainer, model, batch, batch_index)

    @contextlib.contextmanager
    def forward_context(self):
        with contextlib.ExitStack() as stack:
            for plugin in self._plugins:
                if hasattr(plugin, 'forward_context'):
                    ctx = plugin.forward_context()
                    if ctx:
                        stack.enter_context(ctx)
            yield
