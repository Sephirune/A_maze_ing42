from __future__ import annotations

import ctypes
import os
import sys
import time

from cell import EAST, NORTH, SOUTH, WEST, Cell
from generator import MazeGenerator
from maze import Maze
from solver import mark_path, shortest_path

cell_size: int = 35
wall_thickness: int = 2

color_wall: int = 0xFFFFFFFF
color_floor: int = 0x000000FF
color_entry: int = 0x00FF00FF
color_exit: int = 0xFF0000FF
color_path: int = 0x00FFFFFF
color_blocked: int = 0x777777FF

color_list: list[int] = [
    0xFFFFFFFF,
    0xFFAA00FF,
    0x00FF00FF,
    0x4444FFFF,
]


def load_mlx() -> ctypes.CDLL:
    """Load MiniLibX library."""
    path: str = os.path.join(os.path.dirname(__file__), "lib", "libmlx42.so")
    return ctypes.CDLL(path)


class MlxDisplay:
    """Handles MiniLibX display of the maze."""

    def __init__(
        self,
        maze: Maze,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int | None,
        perfect: bool,
    ) -> None:
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect

        self.lib = load_mlx()
        self.setup_signatures()

        self.color_index = 0
        self.wall_color = color_wall
        self.show_path = True
        self.last_key: int | None = None

        self.win_width = maze.width * cell_size
        self.win_height = maze.height * cell_size

        self.mlx = self.lib.mlx_init(
            self.win_width, self.win_height, b"A-Maze-ing", True
        )
        if not self.mlx:
            print("Error: failed to initialize MLX.")
            sys.exit(1)

        self.img = self.lib.mlx_new_image(self.mlx, self.win_width, self.win_height)
        if not self.img:
            print("Error: failed to create image.")
            sys.exit(1)

        if self.lib.mlx_image_to_window(self.mlx, self.img, 0, 0) == -1:
            print("Error: failed to attach image to window.")
            sys.exit(1)

        self.path_dirs = shortest_path(self.maze, self.entry, self.exit)
        if self.show_path:
            mark_path(self.maze, self.entry, self.path_dirs)

        self.draw_maze(self.maze)

    def setup_signatures(self) -> None:
        """Set ctypes signatures."""
        self.lib.mlx_init.restype = ctypes.c_void_p
        self.lib.mlx_init.argtypes = [
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_char_p,
            ctypes.c_bool
        ]

        self.lib.mlx_new_image.restype = ctypes.c_void_p
        self.lib.mlx_new_image.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_uint32
        ]

        self.lib.mlx_image_to_window.restype = ctypes.c_int
        self.lib.mlx_image_to_window.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int
        ]

        self.lib.mlx_put_pixel.restype = None
        self.lib.mlx_put_pixel.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_uint32,
            ctypes.c_uint32
        ]

        self.lib.mlx_loop.restype = None
        self.lib.mlx_loop.argtypes = [ctypes.c_void_p]

        self.lib.mlx_key_hook.restype = None
        self.lib.mlx_key_hook.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p
        ]

        self.lib.mlx_close_window.restype = None
        self.lib.mlx_close_window.argtypes = [ctypes.c_void_p]

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        """Draw one pixel if inside the image."""
        if 0 <= x < self.win_width and 0 <= y < self.win_height:
            self.lib.mlx_put_pixel(self.img, x, y, color)

    def draw_rectangle(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: int,
    ) -> None:
        """Draw and fill a rectangle."""
        if x1 > x2 or y1 > y2:
            return

        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.draw_pixel(x, y, color)

    def draw_hline(self, x1: int, x2: int, y: int, color: int) -> None:
        """Draw a horizontal line."""
        for x in range(x1, x2 + 1):
            self.draw_pixel(x, y, color)

    def draw_vline(self, x: int, y1: int, y2: int, color: int) -> None:
        """Draw a vertical line."""
        for y in range(y1, y2 + 1):
            self.draw_pixel(x, y, color)

    def get_cell_background(self, cell: Cell) -> int:
        """Choose the background color for one cell."""
        if cell.is_blocked:
            return color_blocked
        if cell.is_entry:
            return color_entry
        if cell.is_exit:
            return color_exit
        if cell.is_path and self.show_path:
            return color_path
        return color_floor

    def draw_cell(self, cell: Cell) -> None:
        """Draw one maze cell from its state and walls."""
        x1: int = cell.col * cell_size
        y1: int = cell.row * cell_size
        x2: int = x1 + cell_size - 1
        y2: int = y1 + cell_size - 1

        self.draw_rectangle(x1, y1, x2, y2, self.get_cell_background(cell))

        for offset in range(wall_thickness):
            if cell.has_wall(NORTH):
                self.draw_hline(x1, x2, y1 + offset, self.wall_color)
            if cell.has_wall(SOUTH):
                self.draw_hline(x1, x2, y2 - offset, self.wall_color)
            if cell.has_wall(WEST):
                self.draw_vline(x1 + offset, y1, y2, self.wall_color)
            if cell.has_wall(EAST):
                self.draw_vline(x2 - offset, y1, y2, self.wall_color)

    def clear_image(self) -> None:
        """Clear the image."""
        self.draw_rectangle(
            0,
            0,
            self.win_width - 1,
            self.win_height - 1,
            color_floor,
        )

    def draw_maze(self, maze: Maze) -> None:
        """Draw the full maze."""
        self.maze = maze
        self.clear_image()

        for row in maze.grid:
            for cell in row:
                self.draw_cell(cell)

    def regenerate(self) -> None:
        """Generate and draw a new maze."""
        next_seed: int | None = None if self.seed is None else self.seed + 1
        self.seed = next_seed

        generator = MazeGenerator(
            width=self.maze.width,
            height=self.maze.height,
            entry=self.entry,
            exit=self.exit,
            seed=self.seed,
            perfect=self.perfect,
        )
        self.maze = generator.generate()
        self.path_dirs = shortest_path(self.maze, self.entry, self.exit)

        if self.show_path:
            mark_path(self.maze, self.entry, self.path_dirs)

        self.draw_maze(self.maze)
        print(f"Regenerated maze with seed={self.seed}")

    def handle_key(self):
        """Handles the key choices"""
        self.last_key = None

        @ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
        def keys(key, param):
            if self.last_key == key:
                return

            self.last_key = key

            if key == 256:  # ESC
                print("Exit")
                self.lib.mlx_close_window(self.mlx)

            elif key == 82:  # R
                self.regenerate()

            elif key == 80:  # P
                self.show_path = not self.show_path
                print(f"Show path: {self.show_path}")
                self.path_dirs = shortest_path(self.maze, self.entry, self.exit)
                if self.show_path:
                    mark_path(self.maze, self.entry, self.path_dirs)
                else:
                    for row in self.maze.grid:
                        for cell in row:
                            cell.is_path = False
                self.draw_maze(self.maze)

            elif key == 67:  # C
                self.color_index = (self.color_index + 1) % len(color_list)
                self.wall_color = color_list[self.color_index]
                print(f"Wall color index: {self.color_index}")
                self.draw_maze(self.maze)

        self.lib.mlx_key_hook(self.mlx, keys, None)
        self.keys_call_back = keys  # Se guarda para que no la elimine el garbage collector

    def run(self) -> None:
        """Register callbacks and start MLX loop."""
        self.handle_key()
        self.lib.mlx_loop(self.mlx)
