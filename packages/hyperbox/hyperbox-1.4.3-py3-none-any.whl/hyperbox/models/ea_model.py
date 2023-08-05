from typing import Any, List, Optional, Union

import hydra
import torch
from omegaconf import DictConfig
from pytorch_lightning import LightningModule
from torchmetrics.classification.accuracy import Accuracy

from hyperbox.utils.logger import get_logger
from .base_model import BaseModel

logger = get_logger(__name__)


class EACallback(Callback):

    def on_fit_start(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        if pl_module.kd_subnets_method=='teacher':
            trainer.teacher_net = pl_module.network.copy().to(pl_module.device)
            trainer.teacher_net.eval()
            pl_module.__class__.teacher_net = property(lambda self: self.trainer.teacher_net)

    def on_train_epoch_start(self, trainer, pl_module):
        if trainer.current_epoch >= pl_module.mutator.warmup_epochs:
            pl_module.mutator.start_evolve = True

    def on_train_epoch_end(self, trainer: 'pl.Trainer', pl_module: 'pl.LightningModule'):
        if pl_module.lr_schedulers() is not None:
            self.scheduler = pl_module.lr_schedulers()
            if 'Plateau' in self.scheduler.__class__.__name__:
                if self.scheduler.mode == 'max':
                    self.scheduler.step(pl_module.crt_acc_valid)
                else:
                    self.scheduler.step(pl_module.crt_loss_valid)
                for group in pl_module.optimizer.param_groups:
                    lr = group['lr']
                    break
            else:
                self.scheduler.step(trainer.current_epoch)
                lr = self.scheduler.get_lr()[0]
            logger.info(f"Epoch{trainer.current_epoch} lr={lr:.6f}")

    def on_test_epoch_start(self, trainer, pl_module):
        pl_module.reset_running_statistics()


class EAModel(BaseModel):

    def __init__(
        self,
        network_cfg: Optional[Union[DictConfig, dict]] = None,
        mutator_cfg: Optional[Union[DictConfig, dict]] = None,
        optimizer_cfg: Optional[Union[DictConfig, dict]] = None,
        loss_cfg: Optional[Union[DictConfig, dict]] = None,
        metric_cfg: Optional[Union[DictConfig, dict]] = None,
        scheduler_cfg: Optional[Union[DictConfig, dict]] = None,
        is_sync: bool = True,
        is_net_parallel: bool = True,
        **kwargs
    ):
        r'''Evolutionary Algorithm NAS model
        Args:
            network [DictConfig, dict, torch.nn.Module]: 
            mutator [DictConfig, dict, BaseMutator]: 
            optimizer [DictConfig, dict, torch.optim.Optimizer]: 
            loss Optional[DictConfig, dict, Callable]: loss function or DictConfig of loss function
            metric: metric function, such as Accuracy, Precision, etc.
        '''
        super().__init__(network_cfg, mutator_cfg, optimizer_cfg,
                         loss_cfg, metric_cfg, scheduler_cfg, **kwargs)
        self.is_sync = is_sync
        self.is_net_parallel = is_net_parallel

    def sample_search(self):
        super().sample_search(self.is_sync, self.is_net_parallel)

    def forward(self, x: torch.Tensor):
        return self.network(x)

    def step(self, batch: Any):
        x, y = batch
        logits = self.forward(x)
        loss = self.criterion(logits, y)
        preds = torch.argmax(logits, dim=1)
        return loss, preds, y

    def training_step(self, batch: Any, batch_idx: int):
        self.network.train()
        self.mutator.eval()
        if batch_idx % 1 == 0:
            self.sample_search()
        loss, preds, targets = self.step(batch)

        # log train metrics
        acc = self.train_metric(preds, targets)
        self.log("train/loss", loss, on_step=True, on_epoch=True, prog_bar=False)
        self.log("train/acc", acc, on_step=True, on_epoch=True, prog_bar=False)

        # we can return here dict with any tensors
        # and then read it in some callback or in training_epoch_end() below
        # remember to always return loss from training_step, or else backpropagation will fail!
        return {"loss": loss, "preds": preds, "targets": targets}

    def validation_step(self, batch: Any, batch_idx: int):
        loss, preds, targets = self.step(batch)

        # log val metrics
        acc = self.val_metric(preds, targets)
        self.log("val/loss", loss, on_step=True, on_epoch=True, prog_bar=False)
        self.log("val/acc", acc, on_step=True, on_epoch=True, prog_bar=False)

        return {"loss": loss, "preds": preds, "targets": targets}

    def test_step(self, batch: Any, batch_idx: int):
        loss, preds, targets = self.step(batch)

        # log test metrics
        acc = self.test_metric(preds, targets)
        self.log("test/loss", loss, on_step=False, on_epoch=True)
        self.log("test/acc", acc, on_step=False, on_epoch=True)

        return {"loss": loss, "preds": preds, "targets": targets}

    def test_epoch_end(self, outputs: List[Any]):
        pass

    def configure_callbacks(self):
        ea_callback = EACallback()
        return [
            ea_callback
        ]
