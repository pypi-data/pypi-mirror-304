from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    TypeAlias,
    TypeVar,
    Union,
)

import numpy as np
import torch
from lightning.fabric import Fabric
from lightning.fabric.wrappers import _FabricModule, _FabricOptimizer
from simple_inject import Inject, auto_inject
from torch import nn
from torch.utils.data import DataLoader

from zyplib.train.metric.torch_metric import TorchMetricRecorder
from zyplib.train.utils import step_lr_sched
from zyplib.utils.progress_bar import rich_progress

# 类型定义
Batch: TypeAlias = tuple[torch.Tensor, ...]
Metrics: TypeAlias = Dict[str, float]
T = TypeVar('T')


class MetricRecorder(Protocol):
    def update(
        self, y_pred: torch.Tensor, y: torch.Tensor, loss: float | None = None
    ) -> Metrics: ...
    def compute(self) -> Metrics: ...
    def reset(self) -> None: ...


@dataclass
class FabricTrainingContext:
    """训练上下文对象，用于存储训练相关的状态和配置


    Attributes:
    ----------
    - `model` : `nn.Module`
        - 模型
    - `optimizer` : `torch.optim.Optimizer`
        - 优化器
    - `fabric` : `Fabric | None`, optional
        - 可选项, 如果传入了, 则会调用 fabric 的 `backward` 和 `callback`
    - `train_metric_recorder` : `TorchMetricRecorder | None`, optional
        - 用于记录训练时指标的 recorder 实例，默认为 None
    - `val_metric_recorder` : `TorchMetricRecorder | None`, optional
        - 用于记录验证时指标的 recorder 实例，默认为 None
    """

    model: nn.Module
    optimizer: torch.optim.Optimizer
    fabric: Optional[Fabric] = None
    train_metric_recorder: Optional[MetricRecorder] = None
    val_metric_recorder: Optional[MetricRecorder] = None

    def __post_init__(self):
        if self.fabric is None:
            return

        flag1 = isinstance(self.model, _FabricModule)
        flag2 = isinstance(self.optimizer, _FabricOptimizer)
        if flag1 and flag2:
            return
        elif (not flag1) and (not flag2):
            self.model, self.optimizer = self.fabric.setup(self.model, self.optimizer)
        else:
            raise RuntimeError('FabricTrainingContext 被错误地初始化了')


def _safe_mean(values: list[float]) -> float:
    """安全计算平均值，处理空列表情况"""
    return float(np.mean(values)) if values else 0.0


def training_step(
    ctx: FabricTrainingContext,
    batch: Batch,
    fn_loss: nn.Module,
    batch_idx: Optional[int] = None,
    **kwargs,
) -> Dict[str, Any]:
    """单个训练步骤

    Parameters
    ----------
    - `ctx` : `procedure.FabricTrainingContext`
    - `batch` : `tuple[torch.Tensor, torch.Tensor]`
        - 数据批次
    - `fn_loss` : `nn.Module`
        - 损失函数: `fn_loss(y_pred, y)`
    - `batch_idx`: int

    Returns
    ----------
    - `Dict[str, Any]`: 计算的指标; 至少包含 `loss`
    """
    ctx.model.train()
    x, y = batch

    ctx.optimizer.zero_grad()
    y_pred = ctx.model(x)
    loss: torch.Tensor = fn_loss(y_pred, y)

    if ctx.fabric:
        ctx.fabric.backward(loss)
    else:
        loss.backward()

    ctx.optimizer.step()

    loss_value = loss.item()

    if ctx.train_metric_recorder:
        return ctx.train_metric_recorder.update(y_pred, y, loss_value)
    return {'loss': loss_value}


def validation_step(
    ctx: FabricTrainingContext,
    batch: Batch,
    fn_loss: nn.Module,
    batch_idx: Optional[int] = None,
    **kwargs,
) -> Dict[str, Any]:
    """单个验证步骤

    Parameters
    ----------
    - `ctx` : `procedure.FabricTrainingContext`
    - `batch` : `tuple[torch.Tensor, torch.Tensor]`
        - 数据批次
    - `fn_loss` : `nn.Module`
        - 损失函数: `fn_loss(y_pred, y)`
    - `batch_idx`: int

    Returns
    ----------
    - `Dict[str, Any]`: 计算的指标; 至少包含 `loss`
    """
    ctx.model.eval()
    with torch.no_grad():
        x, y = batch
        y_pred = ctx.model(x)
        loss: torch.Tensor = fn_loss(y_pred, y)

    loss_value = loss.item()
    if ctx.val_metric_recorder:
        return ctx.val_metric_recorder.update(y_pred, y, loss_value)
    return {'loss': loss_value}


@auto_inject
def train_epoch(
    ctx: FabricTrainingContext,
    train_loader: DataLoader,
    fn_loss: nn.Module,
    epoch_idx: Optional[int] = None,
    fn_train_step: Optional[Callable] = Inject('training_step', namespace='train'),
    **train_step_kwargs: Any,
) -> Dict[str, float]:
    """单个训练轮次

    Parameters
    ----------
    - `ctx` : `procedure.FabricTrainingContext`
    - `train_loader` : `DataLoader`
        - 训练数据加载器
    - `fn_loss` : `nn.Module`
        - 损失函数
    - `epoch_idx` : `int | None`, optional
        - 当前轮次索引, 默认为 None
    - `fn_train_step` : `(...) -> Dict[str, Any]`, optional
        - 可选项, 用于计算单个训练步骤的函数, 默认为 `training_step`

    `fn_train_step`:
    ----------
    - @AutoInject: 从 `namespace=train` 自动获取 `training_step`
    - 默认不提供, 使用 `procedure.training_step`; 如果提供了, 则使用提供的函数
    - 接受以下的关键字参数: `fn(ctx: FabricTrainingContext, batch, fn_loss, batch_idx)`
    - 返回值: `Dict[str, Any]`, 至少包含 `loss`
    Returns
    ----------
    - `Dict[str, float]`: 本 Epoch 的平均指标, 至少包含 `loss`
    """
    if fn_train_step is None:
        fn_train_step = training_step

    if ctx.fabric:
        ctx.fabric.call('on_train_epoch_start', epoch=epoch_idx)

    losses = []
    for idx, batch in enumerate(rich_progress(train_loader, 'Training', color='green')):
        metrics = fn_train_step(
            ctx=ctx, batch=batch, fn_loss=fn_loss, batch_idx=idx, **train_step_kwargs
        )
        if ctx.fabric:
            ctx.fabric.call(
                'on_train_batch_end',
                metrics=metrics,
                batch=batch,
                loss=metrics.get('loss', None),
                batch_idx=idx,
            )
        if ctx.train_metric_recorder is None:
            losses.append(metrics['loss'])

    metrics = (
        ctx.train_metric_recorder.compute()
        if ctx.train_metric_recorder
        else {'loss': _safe_mean(losses)}
    )
    if ctx.fabric:
        ctx.fabric.call('on_train_epoch_end', metrics=metrics, epoch=epoch_idx)
    return metrics


@auto_inject
def val_epoch(
    ctx: FabricTrainingContext,
    val_loader: DataLoader,
    fn_loss: nn.Module,
    epoch_idx: Optional[int] = None,
    fn_val_step: Optional[Callable] = Inject('validation_step', namespace='train'),
    **val_step_kwargs: Any,
) -> Dict[str, float]:
    """单个验证轮次

    Parameters
    ----------
    - `ctx` : `procedure.FabricTrainingContext`
    - `train_loader` : `DataLoader`
        - 训练数据加载器
    - `fn_loss` : `nn.Module`
        - 损失函数
    - `epoch_idx` : `int | None`, optional
        - 当前轮次索引, 默认为 None
    - `fn_val_step` : `(...) -> Dict[str, Any]`, optional
        - 可选项, 用于计算单个训练步骤的函数, 默认为 `validation_step`

    `fn_val_step`:
    ----------
    - @AutoInject: 从 `namespace=train` 自动获取 `validation_step`
    - 默认不提供, 使用 `procedure.validation_step`; 如果提供了, 则使用提供的函数
    - 接受以下的关键字参数: `fn(ctx: FabricTrainingContext, batch, fn_loss, batch_idx)`
    - 返回值: `Dict[str, Any]`, 至少包含 `loss`

    Returns
    ----------
    - `Dict[str, float]`: 本 Epoch 的平均指标, 至少包含 `loss`
    """
    if fn_val_step is None:
        fn_val_step = validation_step

    if ctx.fabric:
        ctx.fabric.call('on_validation_epoch_start', epoch=epoch_idx)

    losses = []
    for idx, batch in enumerate(rich_progress(val_loader, 'Validating', color='blue')):
        metrics = fn_val_step(
            ctx=ctx, batch=batch, fn_loss=fn_loss, batch_idx=idx, **val_step_kwargs
        )
        if ctx.fabric:
            ctx.fabric.call(
                'on_validation_batch_end',
                metrics=metrics,
                batch=batch,
                loss=metrics.get('loss', None),
                batch_idx=idx,
            )
        if ctx.val_metric_recorder is None:
            losses.append(metrics['loss'])

    metrics = (
        ctx.val_metric_recorder.compute()
        if ctx.val_metric_recorder
        else {'loss': _safe_mean(losses)}
    )
    if ctx.fabric:
        ctx.fabric.call('on_validation_epoch_end', metrics=metrics, epoch=epoch_idx)
    return metrics


def train_loop(
    fabric: Fabric,  # 如果使用 train_loop, 则默认必须用 fabric
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    train_loader: DataLoader,
    val_loader: Optional[DataLoader],
    fn_loss: nn.Module,
    max_epochs: int,
    train_metric_recorder: TorchMetricRecorder | None = None,
    val_metric_recorder: TorchMetricRecorder | None = None,
    lr_scheduler: Optional[torch.optim.lr_scheduler._LRScheduler] = None,
    lr_sched_freq: int = 1,
    lr_sched_interval: str = 'epoch',
    return_context: bool = False,
) -> Dict[str, List[float]]:
    """基于 Fabric 的 Train Loop; fabric 为必选参数，如果不想用 fabric 可以自行组合 train_epoch etc.

    依赖注入
    ----------
    可以将 `training_step` 和 `validation_step` 函数注入到 `"train"` namespace 下作；如果不注入，使用默认的训练和验证函数。函数需满足如下签名
    ```py
    # 返回中应当至少包含 {'loss': float}
    fn(ctx: FabricTrainingContext, batch, fn_loss, batch_idx) -> dict[str, float]
    ```

    Parameters
    ----------
    - `fabric` : `Fabric`
        - _description_
    - `optimizer` : `torch.optim.Optimizer`
        - _description_
    - `train_loader` : `DataLoader`
        - _description_
    - `val_loader` : `Optional[DataLoader]`
        - _description_
    - `fn_loss` : `nn.Module`
        - _description_
    - `max_epochs` : `int`
        - _description_
    - `train_metric_recorder` : `TorchMetricRecorder | None`, optional
        - _description_, by default None
    - `val_metric_recorder` : `TorchMetricRecorder | None`, optional
        - _description_, by default None
    - `lr_scheduler` : `Optional[torch.optim.lr_scheduler._LRScheduler]`, optional
        - _description_, by default None
    - `lr_sched_freq` : `int`, optional
        - _description_, by default 1
    - `lr_sched_interval` : `str`, optional
        - _description_, by default 'epoch'

    Returns
    ----------
    - `Dict[str, List[float]]`
        - _description_
    """
    context = FabricTrainingContext(
        model=model,
        optimizer=optimizer,
        fabric=fabric,
        train_metric_recorder=train_metric_recorder,
        val_metric_recorder=val_metric_recorder,
    )

    # model, optimizer = fabric.setup(model, optimizer)
    train_loader = fabric.setup_dataloaders(train_loader)
    if val_loader:
        val_loader = fabric.setup_dataloaders(val_loader)

    fabric.call(
        'on_train_start',
        model=model,
        optimizer=optimizer,
        lr_scheduler=lr_scheduler,
        fabric=fabric,
    )

    for epoch in range(max_epochs):
        fabric.call('on_train_epoch_start', epoch=epoch, max_epochs=max_epochs)

        train_metrics = train_epoch(
            ctx=context, train_loader=train_loader, fn_loss=fn_loss, epoch_idx=epoch
        )

        fabric.call('on_train_epoch_end', metrics=train_metrics, epoch=epoch)

        if val_loader:
            fabric.call('on_validation_epoch_start', epoch=epoch)
            val_metrics = val_epoch(
                ctx=context, val_loader=val_loader, fn_loss=fn_loss, epoch_idx=epoch
            )
            fabric.call('on_validation_epoch_end', metrics=val_metrics, epoch=epoch)
        else:
            val_metrics = None

        if lr_scheduler and lr_sched_interval == 'epoch':
            if (epoch + 1) % lr_sched_freq == 0:
                loss = val_metrics['loss'] if val_metrics else train_metrics['loss']
                step_lr_sched(lr_scheduler, loss)

        fabric.call(
            'on_epoch_end',
            epoch=epoch,
            train_metrics=train_metrics,
            val_metrics=val_metrics,
        )

    fabric.call('on_train_end')

    result = {'train': train_metrics, 'val': val_metrics}
    if return_context:
        result['context'] = context
    return result
