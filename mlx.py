import ctypes
import os
from parser_conf import Mazeconf
from typing import Optional


def load_mlx() -> ctypes.CDLL:
    """Load MiniLibX library"""

    path = os.path.join(os.path.dirname(__file__), "lib", "libmlx42.so")
    return ctypes.CDLL(path)


class MlxDisplay:
    """Handles MiniLibX display of the maze"""

    def __init__(self, config: Mazeconf) -> None:
        
