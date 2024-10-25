from pathlib import Path
from typing import Literal, Protocol

import numpy as np

from zyplib.annotation.event import Event


class EEGFileInterface(Protocol):
    """EEG 文件接口"""

    filepath: Path  # 信号文件路径
    meta: dict  # 信号的元数据
    events: list[Event]  # 信号的标注
    name: str  # 信号的名称
    channels: list[str]  # 信号通道标签, 长度等于 `n_channels`
    n_channels: int  # 信号的通道数量
    srate: float  # 信号的采样率
    t_duration: float  # 信号的时间长度; 单位: 秒
    n_samples: int  # 信号的时间样本数量; n_samples = t_duration * sample_rate
    data: np.ndarray  # 信号数据; 形状为 (n_channels, n_samples)
    units: dict[str, Literal['V', 'uV', 'mV', '?']]

    def get_epoch(self, t_start: float, t_duration: float) -> np.ndarray:
        """获取指定时间范围内的信号数据

        >>> signals.get_epoch(t_start=0, t_duration=1)
        >>> # 获取从0秒到1秒的信号数据

        Parameters
        ----------
        - `t_start` : `float`
            - 开始时间; 单位: 秒
        - `t_duration` : `float`
            - 时间长度; 单位: 秒

        Returns
        ----------
        - `np.ndarray`
            - 信号数据; 形状为 (n_channels, n_samples)
        """

    def get_events(
        self, t_start: float, t_duration: float | None = None
    ) -> list[Event] | None:
        """获取指定时间范围内的标注"""
        ...

    def add_event(self, event: Event): ...

    def delete_event(self, t_onset: float, t_duration: float | None = None): ...

    def pick_event(self, t_at: float, episilon: float = 0.1) -> list[Event]: ...


class EventMixin:
    def __init__(self, events: list[Event] | None = None) -> None:
        events = events or []
        self._events: list[Event] = events

    @property
    def events(self) -> list[Event]:
        return self._events

    def _sort_events(self):
        self._events.sort(key=lambda x: x.onset)

    def get_events(self, t_start: float, t_duration: float | None = None) -> list[Event]:
        self._sort_events()
        events = []
        for event in self._events:
            if t_start <= event.onset <= t_start + t_duration:
                events.append(event)
        return events

    def pick_event(self, t_at: float, episilon: float = 0.1) -> list[Event]:
        """获取在 t_at 附近的标注


        Parameters
        ----------
        - `t_at` : `float`
            - 时间点
        - `episilon` : `float`
            - 时间精度

        Returns
        ----------
        - `list[Event]`
            - 在 t_at 附近的标注
        """
        self._sort_events()
        events = []
        for event in self._events:
            if event.duration is None or event.duration <= episilon:
                if t_at - episilon <= event.onset <= t_at + episilon:
                    events.append(event)
            else:
                if (
                    event.onset - episilon
                    <= t_at
                    <= event.onset + event.duration + episilon
                ):
                    events.append(event)
        return events

    def add_event(self, event: Event):
        if event in self._events:
            return False
        self._events.append(event)

    def delete_event(self, event: Event):
        self._events.remove(event)
