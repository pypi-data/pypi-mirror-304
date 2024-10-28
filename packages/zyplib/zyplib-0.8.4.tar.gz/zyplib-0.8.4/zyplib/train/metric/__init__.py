from torchmetrics import Metric, classification, regression

from .torch_metric import TorchMetricRecorder


def clf_metrics_builder(binary: bool = True) -> dict[str, Metric]:
    """构建并返回分类指标字典。

    Parameters:
    ----------
    - `binary` : `bool`, 可选
        - 指示分类任务是否为二分类。如果为 True，则使用二分类指标。
          如果为 False，则使用一般分类指标。默认为 True。

    Return:
    ----------
    - `dict[str, Metric]`, 键是指标名称（例如 "accuracy", "precision"），值是相应的 `Metric` 对象，
    """
    if binary:
        metrics = {
            'accuracy': classification.BinaryAccuracy(),
            'precision': classification.BinaryPrecision(),
            'recall': classification.BinaryRecall(),
            'f1_score': classification.BinaryF1Score(),
        }
    else:
        metrics = {
            'accuracy': classification.Accuracy(),
            'precision': classification.Precision(),
            'recall': classification.Recall(),
            'f1_score': classification.F1Score(),
        }

    return metrics


def reg_metrics_builder() -> dict[str, Metric]:
    """构建并返回回归指标字典。

    Return:
    ----------
    - `dict[str, Metric]`, 键是指标名称（例如 "mae", "mse"），值是相应的 `Metric` 对象。
    """
    metrics = {
        'mae': regression.MeanAbsoluteError(),
        'mse': regression.MeanSquaredError(),
        'rmse': regression.MeanSquaredError(squared=False),  # RMSE 是 MSE 的平方根
        'r2_score': regression.R2Score(),
    }
    return metrics


__all__ = ['TorchMetricRecorder', 'clf_metrics_builder', 'reg_metrics_builder']
