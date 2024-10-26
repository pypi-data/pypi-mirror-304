import torch
import torch.nn as nn
import torch.nn.functional as F
import wandb
from mlconfig import register
from torch.optim import Optimizer
from torch.optim.lr_scheduler import LRScheduler
from torch.utils.data import DataLoader
from torchmetrics import MeanMetric
from torchmetrics.classification import MulticlassAccuracy
from tqdm import tqdm
from tqdm import trange

from ..types import PathLike
from .trainer import Trainer


@register
class ImgoriTrainer(Trainer):
    def __init__(
        self,
        device: torch.device,
        model: nn.Module,
        optimizer: Optimizer,
        scheduler: LRScheduler,
        train_loader: DataLoader,
        valid_loader: DataLoader,
        num_epochs: int,
        num_classes: int,
    ) -> None:
        self.device = device
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.train_loader = train_loader
        self.valid_loader = valid_loader
        self.num_epochs = num_epochs
        self.num_classes = num_classes

        self.state = {"epoch": 1}
        self.metrics = {"best_acc": 0.0}

    def fit(self) -> None:
        start_epoch = self.state["epoch"]
        for epoch in trange(start_epoch, self.num_epochs + 1):
            self.train()
            self.validate()
            self.scheduler.step()

            wandb.log(self.metrics, step=epoch)

            format_string = f"Epoch: {epoch}/{self.num_epochs}"
            for k, v in self.metrics.items():
                format_string += f", {k}: {v:.4f}"
            tqdm.write(format_string)

            self.state["epoch"] = epoch + 1

    def train(self) -> None:
        self.model.train()

        loss_metric = MeanMetric()
        acc_metric = MulticlassAccuracy(num_classes=self.num_classes)

        for x, y in tqdm(self.train_loader):
            x = x.to(self.device)
            y = y.to(self.device)

            output = self.model(x)
            loss = F.cross_entropy(output, y)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            loss_metric.update(loss.cpu(), weight=x.size(0))
            acc_metric.update(output.cpu(), y.cpu())

        self.metrics.update(
            train_loss=float(loss_metric.compute()),
            train_acc=float(acc_metric.compute()),
        )

        del loss_metric
        del acc_metric

    @torch.no_grad()
    def validate(self) -> None:
        self.model.eval()

        loss_metric = MeanMetric()
        acc_metric = MulticlassAccuracy(num_classes=self.num_classes)

        for x, y in tqdm(self.valid_loader):
            x = x.to(self.device)
            y = y.to(self.device)

            output = self.model(x)
            loss = F.cross_entropy(output, y)

            loss_metric.update(loss.cpu(), weight=x.size(0))
            acc_metric.update(output.cpu(), y.cpu())

        valid_acc = float(acc_metric.compute())
        if valid_acc > self.metrics["best_acc"]:
            self.metrics["best_acc"] = valid_acc
            self.save_checkpoint("best.pth")

        self.metrics.update(
            valid_loss=float(loss_metric.compute()),
            valid_acc=valid_acc,
        )

        del loss_metric
        del acc_metric

    def save_checkpoint(self, f: PathLike) -> None:
        self.model.eval()

        checkpoint = {
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "scheduler": self.scheduler.state_dict(),
            "state": self.state,
            "metrics": self.metrics,
        }

        torch.save(checkpoint, f)
        wandb.save(f)

    def resume(self, f: PathLike) -> None:
        checkpoint = torch.load(f, map_location=self.device, weights_only=True)

        self.model.load_state_dict(checkpoint["model"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.scheduler.load_state_dict(checkpoint["scheduler"])
        self.state = checkpoint["state"]
        self.metrics = checkpoint["metrics"]
