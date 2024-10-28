import os
import re
from pathlib import Path

import numpy as np
import scipy.io as sio
from mne.io import read_raw_edf

from zyplib.annotation.event import Event

from ._base import EventMixin


class EDFFile(EventMixin):
    def __init__(self, filepath: str, events: list[Event] | None = None, **mne_kwargs):
        EventMixin.__init__(self, events)
        self.filepath = Path(filepath)
        options = {'verbose': False, 'preload': False}
        options = {**options, **mne_kwargs}
        self.raw = read_raw_edf(filepath, **options)
        self._resolve_raw()

    def _resolve_raw(self):
        # 1. 从 raw 中提取事件
        events = self.raw.annotations
        for event in events:
            self.add_event(Event(event['description'], event['onset'], event['duration']))

    @property
    def meta(self) -> dict:
        return {
            'filepath': self.filepath,
            'n_channels': self.n_channels,
            'srate': self.srate,
            't_duration': self.t_duration,
        }

    @property
    def name(self) -> str:
        return os.path.basename(self.filepath)

    @property
    def channels(self) -> list[str]:
        return self.raw.ch_names

    @property
    def n_channels(self) -> int:
        return len(self.raw.ch_names)

    @property
    def srate(self) -> float:
        return self.raw.info['sfreq']

    @property
    def t_duration(self) -> float:
        return self.raw.times[-1]

    @property
    def n_samples(self) -> int:
        return self.raw.n_times

    @property
    def data(self) -> np.ndarray:
        return self.raw.get_data()

    @property
    def units(self):
        return {ch['ch_name']: ch['unit'] for ch in self.raw.info['chs']}

    def get_epoch(self, t_start: float, t_duration: float, units='uV') -> np.ndarray:
        start_sample = int(t_start * self.srate)
        end_sample = start_sample + int(t_duration * self.srate)
        return self.raw.get_data(start=start_sample, stop=end_sample, units=units)
