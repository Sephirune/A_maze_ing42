import ctypes
import os
from parser_conf import Mazeconf
from typing import Optional

cell_size: int = 20
color_wall: int = 0xFFFFFFFF  # Blanco
color_floor: int = 0x000000FF  # Negro
color_entry: int = 0x00FF00FF  # Verde
color_exit: int = 0xFF0000FF  # Rojo
color_path: int = 0x00FFFFFF  # Cian

color_list: list[int] = [
    0xFFFFFFFF,  # Blanco
    0xFFAA00FF,  # Naranja
    0x00FF00FF,  # Verde
    0x4444FFFF,  # Azul
]

# Coordenadas según los bits:
# 0b0001: Norte
# 0b0010: Este
# 0b0100: Sur
# 0b1000: Oeste


def load_mlx() -> ctypes.CDLL:
    """Load MiniLibX library"""

    path = os.path.join(os.path.dirname(__file__), "lib", "libmlx42.so") # si no encuentra la libreria: OSError.
    return ctypes.CDLL(path)


class MlxDisplay:
    """Handles MiniLibX display of the maze"""

    def __init__(self, config: Mazeconf) -> None:
        """Initialize MLX windows and image buffer"""

        self.config = config  # Config va a ser la config validada
        self.lib = load_mlx()
        

