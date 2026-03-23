import ctypes
import os
import sys
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

    path = os.path.join(os.path.dirname(__file__), "lib", "libmlx42.so") # si no encuentra la libreria da: OSError.
    return ctypes.CDLL(path)


def handle_colors(colors: list[str], index: int) -> int:
    """Cycle to the next wall color and print it"""

    index = (index + 1) % len(colors)
    print(f"Next color -> {colors[index]}")
    return index


class MlxDisplay:
    """Handles MiniLibX display of the maze"""

    def __init__(self, config: Mazeconf) -> None:
        """Initialize MLX windows and image buffer"""

        self.config = config  # Config va a ser la config validada
        self.lib = load_mlx()
        self.setup_signatures()

        self.win_width = config.width * cell_size
        self.win_height = config.height * cell_size

        # La lógica de esto la he sacado del ejemplo que está en el git de codam. Pasé la lógica de c a python.
        # Cosas como mlx_init o mlx_new_image ya están cargadas en el so de la librería, así que esto es más fácil.
        self.mlx = self.lib.mlx_init(self.win_width, self.win_height, b"A-Maze-ing",
                                     True)
        if not self.mlx:
            print("Error: Failed to load mlx init.")
            sys.exit(1)

        self.img = self.lib.mlx_new_image(self.mlx, self.win_width, self.win_height,)

        if not self.img:
            print("Error: Failed to load img.")
            sys.exit(1)

        if self.lib.mlx_image_to_window(self.mlx, self.img, 0, 0) == -1:
            print("Error: Failed to create window")
            sys.exit(1)

    def setup_signatures(self) -> None:
        """Fixes an error in python with the ctypes and the pointer-return.
        In C, the compiler knows that mlx_init returns a pointer to mlx_t.
        In python, ctypes assumes it returns an int, which
        corrupts 64-bit pointers."""

        self.lib.mlx_init.restype = ctypes.c_void_p
        self.lib.mlx_new_image.restype = ctypes.c_void_p
        self.lib.mlx_image_to_window.restype = ctypes.c_int

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        """Draw a pixel on the map"""

        self.lib.mlx_put_pixel(self.img, x, y, color)

    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, color: int) -> None:
        """Draw and fill a rectangle"""

        if x1 > x2 or y1 > y2:
            print("Error: Invalid size.")
            sys.exit(1)

        try:
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    self.draw_pixel(self.mlx, x, y, color)
        except ValueError:
            print("Error filling the matrix.")
            sys.exit(1)

    def draw_cell(self, row: int, col: int, color: int) -> None:
        """Creates and fills cells"""

        x1 = row * cell_size
        y1 = col * cell_size
        x2 = x1 * cell_size - 1
        y2 = y1 * cell_size - 1

        self.draw_rectangle(self.mlx, x1, y1, x2, y2, color)
    
    def draw_maze(self, x: int, y: int, color: int) -> None:
        """Draws the whole maze"""
        
        self.draw_rectangle()