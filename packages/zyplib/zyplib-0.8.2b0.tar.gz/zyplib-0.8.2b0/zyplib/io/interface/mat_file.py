import os
import re
from pathlib import Path

import numpy as np
import scipy.io as sio

from zyplib.annotation.event import Event

from ._base import EventMixin


class MatFile(EventMixin):
    DATA_PAT = r'^data(.*)'
    LABEL_PAT = r'^(channel|label)s?'
    SRATE_PAT = r'^(srate|sfreq|freq|sample_rate)s?'

    def __init__(
        self,
        filepath: str,
        srate: float | None = None,
        channels: list[str] | None = None,
        events: list[Event] | None = None,
        key_data: str | None = None,
        key_channels: str | None = None,
        key_srate: str | None = None,
        **kwargs,
    ):
        EventMixin.__init__(self, events)
        self.filepath = Path(filepath)

        self.data = None
        self.srate = srate
        self.channels = channels
        self.n_channels = 0
        self.n_samples = 0
        self.t_duration = 0

        self.name = os.path.basename(filepath)
        self.meta = {}

        try:
            mat = sio.loadmat(filepath)
            mat = {k: v for k, v in mat.items() if not k.startswith('__')}
            self._resolve_mat(mat, key_data, key_channels, key_srate)
        except Exception as e:
            raise RuntimeError(f'文件读取错误: {e}')

        self.n_samples = self.data.shape[1]
        self.t_duration = self.n_samples / self.srate

    def _resolve_mat(
        self,
        mat: dict,
        key_data: str | None,
        key_channels: str | None,
        key_srate: str | None,
    ):
        keys = list(mat.keys())

        # Use provided keys if available
        if key_data and key_data in mat:
            data = mat[key_data]
        else:
            for key in keys:
                if re.match(self.DATA_PAT, key):
                    data = mat[key]
                    break

        if key_channels and key_channels in mat:
            self.channels = mat[key_channels]
        else:
            for key in keys:
                if re.match(self.LABEL_PAT, key):
                    self.channels = mat[key]
                    break

        if key_srate and key_srate in mat:
            self.srate = mat[key_srate]
        else:
            for key in keys:
                if re.match(self.SRATE_PAT, key):
                    self.srate = mat[key]
                    break

        # =============== Section Beg: Data =============== #
        if data.ndim == 1:
            data = data.reshape(1, -1)
        # 数据默认应该是的第一维是通道数，第二维是时间
        CH, T = data.shape
        # 如果通道数大于时间，那么说明数据的第一维是时间，第二维是通道数
        if CH > T:
            data = data.T
            CH, T = data.shape
        self.data = data
        # --------------- Section End: Data --------------- #

        if self.channels is None:
            self.channels = [f'ch{i}' for i in range(CH)]

        if self.srate is None:
            raise RuntimeError('未找到采样率信息')

        self.n_channels = CH
        self.n_samples = T
        self.t_duration = T / self.srate

    def get_epoch(self, t_start: float, t_duration: float) -> np.ndarray:
        idx_start = int(t_start * self.srate)
        idx_end = idx_start + int(t_duration * self.srate)
        return self.data[:, idx_start:idx_end]

    @property
    def units(self):
        return { c: '?' for c in self.channels }
