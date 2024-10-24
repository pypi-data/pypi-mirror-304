__doc__ = """
读写常见的格式的数据文件
"""

from .interface import EDFFile as EDFFileInterface
from .interface import MatFile as MatFileInterface

__all__ = ['EDFFileInterface', 'MatFileInterface']
