from typing import Callable, Dict, List, Literal, Optional

# import matplotlib.pyplot as plt
import torch
from torchmetrics import Metric, MetricCollection

from zyplib.train.utils import prefixed_dict, use_device
from zyplib.utils.ensure import ensure_scalar


class ScalarMetric:
    def __init__(
        self,
        default_reducer: Literal['mean', 'sum'] = 'mean',
        retain_batch_history: bool = False,
        retain_epoch_history: bool = True,
    ):
        """记录单个 float 类型的指标

        唯一的作用是简化「记录 Batch 指标 - 在 epoch 结束后求平均」的工作流程

        Example:
        --------
        >>> metric = ScalarMetric()
        >>> metric.define_metric('loss', reducer='mean')
        >>> for batch in dataloader:
        >>>     y_hat, y = batch
        >>>     loss = compute_loss(y_hat, y)
        >>>     acc = compute_acc(y_hat, y)
        >>>     metric.update(loss=loss.item(), acc=acc)
        >>> metric.compute()  # 得到当前 epoch 的平均损失和准确率
        """
        self._batch_metrics: dict[
            str, list[float]
        ] = {}  # 每个 batch 内的指标, 随着 reset 清空

        self._batch_history: list[dict[str, float]] = []
        self._epoch_history: list[dict[str, float]] = []

        self._metrics: dict[str, Callable[[list[float]], float]] = {}
        self._default_reducer = (
            lambda x: sum(x) / len(x) if default_reducer == 'mean' else sum(x)
        )

        self._retain_batch_history = retain_batch_history
        self._retain_epoch_history = retain_epoch_history

    def define_metric(self, metric_name: str, reducer: Literal['mean', 'sum'] = 'mean'):
        """定义一个新的指标及其计算方式

        Parameters
        ----------
        - `metric_name` : `str`
            - 指标名称
        - `reducer` : `Literal['mean', 'sum']`, optional
            - 计算方式, 默认为 'mean'
        """
        self._batch_metrics[metric_name] = []
        if reducer == 'mean':
            self._metrics[metric_name] = lambda x: sum(x) / len(x)
        elif reducer == 'sum':
            self._metrics[metric_name] = sum
        else:
            raise ValueError("reducer must be either 'mean' or 'sum'")

    def update(self, **metrics: float):
        """更新当前 step 的指标值

        Parameters
        ----------
        **metrics : float
            指标名称和对应的值
        """
        for name, value in metrics.items():
            if name not in self._metrics:
                self._metrics[name] = self._default_reducer
                self._batch_metrics.setdefault(name, [])
            self._batch_metrics[name].append(value)

        if self._retain_batch_history:
            self._batch_history.append(metrics)

    def compute(self) -> dict[str, float]:
        """reduce 当前 batch 的指标

        建议在每个 epoch 结束之后调用, 并且调用 compute 之后需要调用 reset 清空当前 step 的数据

        Returns
        -------
        dict[str, float]
            指标名称和对应的计算结果
        """
        results = {}
        for name, reducer in self._metrics.items():
            if self._batch_metrics[name]:  # 确保有数据
                results[name] = reducer(self._batch_metrics[name])

        # 保存结果并清空当前 step 的数据
        if self._retain_epoch_history:
            self._epoch_history.append(results)

        return results

    def reset(self):
        self._batch_metrics = {name: [] for name in self._metrics.keys()}


class TorchMetricRecorder:
    def __init__(
        self,
        metrics: MetricCollection | dict[str, Metric],
        before_metric: Literal['sigmoid', 'softmax']
        | Callable[[torch.Tensor], torch.Tensor]
        | dict[str | Literal['*'], Callable] = None,
    ):
        """添加基于 `torchmetrics` 的日志评估指标的功能

        Parameters
        ----------
        - `metrics` : `MetricCollection | Dict[str, Metric]`, optional
            - 评估指标
            - 使用 `torchmetrics.MetricCollection` 或 `dict` 类型
        - `before_metric` : `'sigmoid' | 'softmax' | Callable | dict[str, Callable]`, optional

        `before_metric`:
        ----------
        在计算评估指标之前的激活函数: `(y_hat) -> y_activated`

        例如在二分类问题中，模型最后一层没有激活函数, 在计算评估指标 (即 `metrics`) 之前需要使用 `torch.sigmoid` 激活

        - `None`: 不需要额外的激活函数
        - `Literal['sigmoid', 'softmax']`: 使用 torch.sigmoid 和 torch.softmax
        - `(Tensor) -> Tensor`: 指定的激活函数
        - `dict[str, (Tensor) -> Tensor]`: 在比较复杂的情况下, 各个指标使用的输入不同的情况下可以用这个
            - key: 如果为 `*` 则代表通配符
            - value: `(Tensor) -> Tensor`, 为 None，则不激活
        """
        if before_metric == 'sigmoid':
            self.before_metric = torch.sigmoid
        elif before_metric == 'softmax':
            self.before_metric = torch.softmax
        else:
            self.before_metric = before_metric

        # 只保留一个 metrics collection
        if isinstance(metrics, dict):
            self.metrics = MetricCollection(metrics)
        else:
            self.metrics = metrics

        # 记录哪些传入 update 的标量数据, 包括 loss 等
        self.scalar_metrics = ScalarMetric(default_reducer='mean')
        self.scalar_metrics.define_metric('loss', 'mean')  # 预定义 loss 指标

        # self.step_history = {metric_name: [] for metric_name in self.metrics.keys()}
        # self.step_history['loss'] = []
        # self.epoch_history: list[dict[str, float | torch.Tensor]] = []

        self.current_epoch = 0
        self.current_step = 0

    def to_device(self, device: str | torch.device):
        # 简化 to_device，只需要处理一个 metrics collection
        for key, metric in self.metrics.items():
            use_device(metric, device)

    def _apply_activation(
        self, y_hat: torch.Tensor
    ) -> torch.Tensor | dict[str, torch.Tensor]:
        # 处理 before_metric 激活
        if self.before_metric is None:
            y_hat_activated = y_hat
        elif isinstance(self.before_metric, dict):
            # 如果是字典类型，需要对不同的指标使用不同的激活函数
            y_hat_activated = {}
            for metric_name in self.metrics.keys():
                # 检查是否有针对特定指标的激活函数
                if metric_name in self.before_metric:
                    activation_fn = self.before_metric[metric_name]
                # 检查是否有通配符激活函数
                elif '*' in self.before_metric:
                    activation_fn = self.before_metric['*']
                else:
                    activation_fn = None

                if activation_fn is not None:
                    y_hat_activated[metric_name] = activation_fn(y_hat)
                else:
                    y_hat_activated[metric_name] = y_hat
        else:
            # 如果是单个激活函数
            if self.before_metric == torch.softmax:
                # softmax 需要指定 dim 参数
                y_hat_activated = self.before_metric(y_hat, dim=-1)
            else:
                y_hat_activated = self.before_metric(y_hat)
        return y_hat_activated

    def update(self, y_hat, y, loss: Optional[float] = None, **scalar_metrics: float):
        """更新某个 step 的评估指标

        Parameters
        ----------
        - `y_hat` : `torch.Tensor`
            - 预测值
        - `y` : `torch.Tensor`
            - 真实值
        - `loss` : `float?`, optional
            - 损失值
        - `**scalar_metrics` : float
            - 其他标量指标
        """
        result = {}

        # 更新 loss 和其他标量指标
        if loss is not None:
            if isinstance(loss, torch.Tensor):
                loss = loss.item()
            self.scalar_metrics.update(loss=loss)
            result['loss'] = loss

        # 更新其他标量指标
        if scalar_metrics:
            self.scalar_metrics.update(**scalar_metrics)
            result.update(scalar_metrics)

        # 更新 torchmetrics
        y_hat_activated = self._apply_activation(y_hat)
        for metric_name, metric in self.metrics.items():
            if isinstance(y_hat_activated, dict):
                current_y_hat = y_hat_activated[metric_name]
            else:
                current_y_hat = y_hat_activated

            step_metric_value = metric(current_y_hat, y)  # 记录本 step 的指标

            # 记录计算得到的指标
            self._record_compute_value(result, metric_name, step_metric_value)

        self.current_step += 1
        return result

    def compute(self):
        """计算一个 epoch 的评估指标"""
        epoch_metrics = {}

        # 计算标量指标
        scalar_results = self.scalar_metrics.compute()
        epoch_metrics.update(scalar_results)
        self.scalar_metrics.reset()

        # 计算 torchmetrics
        for metric_name, metric in self.metrics.items():
            epoch_metric_value = metric.compute()
            # epoch_metrics[metric_name] = epoch_metric_value.item()
            self._record_compute_value(epoch_metrics, metric_name, epoch_metric_value)
            metric.reset()

        self.current_epoch += 1
        self.current_step = 0
        return epoch_metrics

    def _record_compute_value(
        self,
        recorder: dict[str, float | torch.Tensor],
        name: str,
        value: float | torch.Tensor | dict,
    ):
        """将 metric 计算得到的结果记录在字典当中

        由于 metric 计算得到的结果可能是 dict 类型, 也可能是标量, 所以需要单独处理

        value 如果是 dict, 默认应当是只有一层!
        """
        if isinstance(value, dict):
            recorder.update(prefixed_dict(f'{name}.', value))
        elif value is not None:
            # 能转换成标量就记录标量，不能就记录原值
            scalar = ensure_scalar(value)
            recorder[name] = scalar or value
