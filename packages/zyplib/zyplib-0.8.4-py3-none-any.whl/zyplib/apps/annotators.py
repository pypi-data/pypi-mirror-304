"""
- Background: 进行脑电等时序信号分析, 需要可视化信号、编辑标注信息等
- App: 基于 Tkinter 实现的信号可视化应用界面
- 功能:
    - 可视化信号波形图
    - 可视化标注信息
    - 新建标注
    - 删除标注
"""

import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from zyplib.annotation import Event
from zyplib.io.interface import EEGFileInterface
from zyplib.utils.fs import write_json
from zyplib.utils.print import print_debug
from zyplib.vis import plot_signals


@dataclass
class AppState:
    t_start: float  # 开始时间, 单位: 秒
    t_page: float  # 页面长度, 单位: 秒
    interval: float | None
    active_event: Event | None = None


class TemporaryEventMixin:
    def __init__(self, *args, **kwargs):
        self.temporary_event = None
        self.line_2d = None
        self.span_2d = None

    def plot_temp_event(self, event: Event | None):
        self.temporary_event = event
        self.clear_temp_event()
        if event is None:
            return
        onset = event.onset
        duration = event.duration
        label = event.name
        if duration is None:
            self.line_2d = plt.axvline(onset, color='black', linestyle='--', label=label)
        else:
            self.span_2d = plt.axvspan(
                onset, onset + duration, color='black', alpha=0.2, label=label
            )
        plt.draw()  # 刷新绘图

    def clear_temp_event(self):
        self.temporary_event = None
        if self.line_2d:
            self.line_2d.remove()
            self.line_2d = None
        if self.span_2d:
            self.span_2d.remove()
            self.span_2d = None
        plt.draw()  # Redraw the plot to reflect the changes


class SignalAnnotatorApp(TemporaryEventMixin):
    def __init__(self, signals: EEGFileInterface, fn_on_exit: Callable[[], None]):
        super().__init__()

        self.signals = signals
        self.fn_on_exit = fn_on_exit
        self.state = AppState(t_start=0, t_page=4, interval=None, active_event=None)
        self.root = None
        self.canvas = None
        self.onset_entry = None
        self.duration_entry = None
        self.interval_entry = None

        self.annt_onset_entry = None
        self.annt_duration_entry = None
        self.annt_label_entry = None

    def on_click_figure(self, event):
        """鼠标点击波形图时的回调函数
        行为
        ----------
        - 鼠标左键:
            - 使用 `get_annotation` 方法, 获取在 `at.x` 左右 0.1 秒范围内的标注
            - 如果存在这样的标注, 记为 `state.active_event`
        - 鼠标右键: 在界面中添加新的标注
            - if active_event is None:
                - 在界面中添加新的标注, 更新 onset
                - 此时 active_event 的 onset 已知, duration 未知, 被视为一个新的单点标注
            - else if active_event is not None and active_event.duration is None
                - 更新 active_event.duration
                - 此时 active_event 的 onset 和 duration 都已知, 视为一个区域标注
            - else if active_event 是一个 区域标注
                - 清空 active_event
            - 做完之后, 更新 Figure
        """
        if not event.xdata:
            return
        if event.button == 1:  # 左键点击
            at_x = event.xdata
            annotations = self.signals.pick_event(at_x)
            if annotations:
                self.state.active_event = annotations[0]  # 选中第一个标注
                print_debug(f'选中标注: {self.state.active_event}')
            else:
                self.state.active_event = None
                print_debug('无标注')
            self.clear_temp_event()
            self.update_annotation_fields()
        elif event.button == 3:  # 右键点击
            at_x = event.xdata
            if self.state.active_event is None:
                # 创建新标注
                label_name = self.annt_label_entry.get() or ''
                self.state.active_event = Event(
                    name=label_name, onset=at_x, duration=None
                )
                self.update_annotation_fields()
                print_debug(f'创建新标注: {self.state.active_event}')
            else:
                if self.state.active_event.duration is None:
                    # 更新持续时间
                    self.state.active_event.duration = (
                        at_x - self.state.active_event.onset
                    )
                    print_debug(f'更新标注持续时间: {self.state.active_event}')
                else:
                    self.state.active_event = None  # 清除选中标注
                    print_debug('清除标注')
            self.update_annotation_fields()
            self.plot_temp_event(self.state.active_event)

    def update_plot(self):
        self.clear_temp_event()
        signals_data = self.signals.get_epoch(self.state.t_start, self.state.t_page)
        if self.state.interval is None or self.state.interval == 'auto':
            self.state.interval = 1.5 * np.max(np.abs(signals_data))
            self.update_entry_fields()

        fig = plt.gcf()
        # 清空 fig
        fig.clear()
        plot_signals(
            signals=signals_data,
            srate=int(self.signals.srate),
            labels=self.signals.channels,
            interval=self.state.interval,
            events=self.signals.get_events(self.state.t_start, self.state.t_page),
            t_start=self.state.t_start,
            new_fig=False,
            show=False,
            save_path=None,
        )
        self.canvas.figure = fig
        self.canvas.draw()

        self.state.active_event = None

    def update_entry_fields(self):
        self.onset_entry.delete(0, tk.END)
        self.onset_entry.insert(0, str(self.state.t_start))
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, str(self.state.t_page))

        if self.interval_entry:
            self.interval_entry.delete(0, tk.END)
            self.interval_entry.insert(0, str(self.state.interval))

    def update_annotation_fields(self):
        event = self.state.active_event
        if event is None:
            self.annt_onset_entry.delete(0, tk.END)
            self.annt_duration_entry.delete(0, tk.END)
            # self.annt_label_entry.delete(0, tk.END)
            return

        self.annt_onset_entry.delete(0, tk.END)
        self.annt_onset_entry.insert(0, str(event.onset))

        if event.duration is not None:
            self.annt_duration_entry.delete(0, tk.END)
            self.annt_duration_entry.insert(0, str(event.duration))

        if event.name:
            self.annt_label_entry.delete(0, tk.END)
            self.annt_label_entry.insert(0, event.name)

    def load_left(self):
        if self.state.t_start == 0:
            messagebox.showinfo('信息', '已到达左边界')
            return
        new_t_start = self.state.t_start - self.state.t_page
        if new_t_start < 0:
            new_t_start = 0
        self.state.t_start = new_t_start
        self.state.active_event = None
        self.update_entry_fields()
        self.update_annotation_fields()
        self.update_plot()

    def load_right(self):
        if self.state.t_start + self.state.t_page >= self.signals.t_duration:
            messagebox.showinfo('信息', '已到达右边界')
            return
        self.state.t_start += self.state.t_page
        if self.state.t_start + self.state.t_page > self.signals.t_duration:
            self.state.t_start = self.signals.t_duration - self.state.t_page
            messagebox.showinfo('信息', '已到达右边界')

        self.state.active_event = None
        self.update_entry_fields()
        self.update_annotation_fields()
        self.update_plot()

    def add_annotation(self):
        if self.state.active_event is None:
            return
        self.signals.add_event(self.state.active_event)
        self.state.active_event = None
        self.update_annotation_fields()
        self.update_plot()

    def delete_annotation(self):
        if self.state.active_event is None:
            return
        self.signals.delete_event(self.state.active_event)
        self.state.active_event = None
        self.update_annotation_fields()
        self.update_plot()

    def build_tk_ui(self):
        self.root = tk.Tk()
        self.root.title('脑电信号可视化')
        # self.root.geometry('1000x600')

        # ========================= 信息显示区  ========================= #
        info_frame = ttk.Frame(self.root)
        info_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(info_frame, text='信号名称: ' + self.signals.name).pack(side=tk.LEFT)
        ttk.Label(info_frame, text='通道标签: ' + ', '.join(self.signals.channels)).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Label(info_frame, text='采样率: ' + str(self.signals.srate)).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Label(info_frame, text='时间长度: ' + str(self.signals.t_duration)).pack(
            side=tk.LEFT, padx=5
        )

        # 退出按钮
        ttk.Button(info_frame, text='退出', command=self.root.quit).pack(side=tk.RIGHT)
        ttk.Button(info_frame, text='保存', command=self.save_annotations).pack(
            side=tk.RIGHT
        )

        # ========================= 图形区  ========================= #
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ========================= 按钮区  ========================= #
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # --------------- 下部左侧 --------------- #
        ttk.Button(button_frame, text='向左加载', command=self.load_left).pack(
            side=tk.LEFT
        )
        ttk.Button(button_frame, text='向右加载', command=self.load_right).pack(
            side=tk.LEFT
        )

        def update_state(onset=None, duration=None, interval=None):
            self.state.t_start = onset or self.state.t_start
            self.state.t_page = duration or self.state.t_page
            self.state.interval = interval or self.state.interval

        ttk.Label(button_frame, text='开始时间:').pack(side=tk.LEFT)
        self.onset_entry = ttk.Entry(button_frame)
        self.onset_entry.pack(side=tk.LEFT)
        self.onset_entry.bind(
            '<KeyRelease>',
            lambda event: update_state(onset=float(self.onset_entry.get())),
        )

        ttk.Label(button_frame, text='持续时间:').pack(side=tk.LEFT)
        self.duration_entry = ttk.Entry(button_frame)
        self.duration_entry.pack(side=tk.LEFT)
        self.duration_entry.bind(
            '<KeyRelease>',
            lambda event: update_state(duration=float(self.duration_entry.get())),
        )

        ttk.Label(button_frame, text='Y轴 Interval:').pack(side=tk.LEFT)
        self.interval_entry = ttk.Entry(button_frame)
        self.interval_entry.pack(side=tk.LEFT)

        def _get_interval():
            interval = self.interval_entry.get()
            if interval:
                return float(interval)
            return 'auto'  # interval 可以为 auto

        self.interval_entry.bind(
            '<KeyRelease>', lambda event: update_state(interval=_get_interval())
        )
        ttk.Button(button_frame, text='刷新', command=self.update_plot).pack(side=tk.LEFT)

        ttk.Label(button_frame, text='\t').pack(side=tk.LEFT)
        # --------------- 下部右侧 --------------- #

        ttk.Label(button_frame, text='标注标签:').pack(side=tk.LEFT)
        self.annt_label_entry = ttk.Entry(button_frame)
        self.annt_label_entry.pack(side=tk.LEFT)

        ttk.Label(button_frame, text='标注开始时间:').pack(side=tk.LEFT)
        self.annt_onset_entry = ttk.Entry(button_frame)
        self.annt_onset_entry.pack(side=tk.LEFT)

        ttk.Label(button_frame, text='标注持续时间:').pack(side=tk.LEFT)
        self.annt_duration_entry = ttk.Entry(button_frame)
        self.annt_duration_entry.pack(side=tk.LEFT)

        ttk.Button(button_frame, text='添加标注', command=self.add_annotation).pack(
            side=tk.LEFT
        )
        ttk.Button(button_frame, text='删除标注', command=self.delete_annotation).pack(
            side=tk.LEFT
        )

        # 绑定图形点击事件
        fig.canvas.mpl_connect('button_press_event', self.on_click_figure)

    def run(self):
        self.build_tk_ui()
        self.update_entry_fields()
        self.update_plot()  # 初始化时更新绘图
        self.root.mainloop()
        # self.fn_save()  # 保存功能的回调

    def save_annotations(self):
        event_fpath = self.signals.filepath.with_suffix('.events.json')

        write_json(event_fpath, [event.to_dict() for event in self.signals.events])
        print(f'保存标注信息到: {event_fpath}')


def _launch_app(signals: EEGFileInterface, fn_on_exit: Callable[[], None] | None = None):
    app = SignalAnnotatorApp(signals, fn_on_exit)
    app.run()


def launch_app(fpath: str | None = None, srate: float | None = None):
    from zyplib.io import EDFFileInterface, MatFileInterface

    from .select_file import launch_app as launch_select_file_app

    def on_file_selected(path: Path):
        print_debug(f'Viz 文件: {path}')
        if path.suffix == '.mat':
            signals = MatFileInterface(path, srate=srate)
        elif path.suffix == '.edf':
            signals = EDFFileInterface(path)
        else:
            raise ValueError(f'不支持的文件类型: {path}')

        _launch_app(signals)

    if fpath is None:
        launch_select_file_app(on_file_selected)
    else:
        on_file_selected(Path(fpath))
