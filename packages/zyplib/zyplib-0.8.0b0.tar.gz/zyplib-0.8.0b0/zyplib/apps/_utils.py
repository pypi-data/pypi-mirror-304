import ctypes

__all__ = ['set_dpi_awareness']


def set_dpi_awareness():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except Exception:
        pass
