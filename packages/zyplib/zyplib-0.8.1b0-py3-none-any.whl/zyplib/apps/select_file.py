import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk
from typing import Callable

from ._utils import set_dpi_awareness


def launch_app(fn_file_cb: Callable[[Path], None]):
    def select_file():
        extensions = extension_entry.get().strip()
        filetypes = [('All files', '*.*')]
        if extensions:
            ext_list = [f'*.{ext.strip()}' for ext in extensions.split(',')]
            filetypes = [('Selected files', ' '.join(ext_list))] + filetypes

        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(), filetypes=filetypes
        )
        if file_path:
            root.destroy()
            fn_file_cb(Path(file_path))

    set_dpi_awareness()
    root = tk.Tk()
    root.title('选择文件')
    root.geometry('400x150')

    frame = ttk.Frame(root, padding='10')
    frame.pack(fill=tk.BOTH, expand=True)

    extension_label = ttk.Label(frame, text='文件后缀 (用逗号 "," 分隔):')
    extension_label.pack(pady=(0, 5))

    extension_entry = ttk.Entry(frame)
    extension_entry.pack(fill=tk.X, pady=(0, 10))
    extension_entry.insert(0, 'mat,edf')

    button = ttk.Button(frame, text='选择文件', command=select_file)
    button.pack(expand=True)

    root.mainloop()


if __name__ == '__main__':

    def fn_file_cb(path: Path):
        print(path)

    launch_app(fn_file_cb)
