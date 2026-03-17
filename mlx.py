import ctypes
import ctypes.util
import os
from parser_conf import Mazeconf


def load_mlx() -> ctypes.CDLL:
    """Load MiniLibX library"""

    path = os.path.join(os.path.dirname(__file__), "libmlx.a")
    return ctypes.CDLL(path)


class MlxDisplay:
    """Handles MiniLibX display of the maze"""
    
    def __init__(self, config: Mazeconf) -> None
    
