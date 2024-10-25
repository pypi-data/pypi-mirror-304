"""统一的信号文件 IO 结构"""
from ._base import EEGFileInterface
from .edf_file import EDFFile
from .mat_file import MatFile
