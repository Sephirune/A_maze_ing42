import ctypes
import os
import sys
from parser_conf import Mazeconf
from cell import Cell, NORTH, EAST, SOUTH, WEST

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
    path = os.path.join(os.path.dirname(__file__), "lib", "libmlx42.so")
    return ctypes.CDLL(path)


class MlxDisplay:
    """Handles MiniLibX display of the maze."""

    def __init__(self, config: Mazeconf) -> None:
        self.config = config
        self.lib = load_mlx()
        self.setup_signatures()

        self.win_width = config.width * cell_size
        self.win_height = config.height * cell_size
        self.wall_color = color_wall
        self.show_path = True

        self.mlx = self.lib.mlx_init(
            self.win_width, self.win_height, b"A-Maze-ing", True
        )
        if not self.mlx:
            print("Error: Failed to load mlx init.")
            sys.exit(1)

        self.img = self.lib.mlx_new_image(
            self.mlx, self.win_width, self.win_height
        )
        if not self.img:
            print("Error: Failed to load img.")
            sys.exit(1)

        if self.lib.mlx_image_to_window(self.mlx, self.img, 0, 0) == -1:
            print("Error: Failed to create window")
            sys.exit(1)

    def setup_signatures(self) -> None:
        """Set ctypes signatures."""
        self.lib.mlx_init.restype = ctypes.c_void_p
        self.lib.mlx_init.argtypes = [
            ctypes.c_int32, ctypes.c_int32, ctypes.c_char_p, ctypes.c_bool
        ]

        self.lib.mlx_new_image.restype = ctypes.c_void_p
        self.lib.mlx_new_image.argtypes = [
            ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32
        ]

        self.lib.mlx_image_to_window.restype = ctypes.c_int
        self.lib.mlx_image_to_window.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int
        ]

        self.lib.mlx_put_pixel.restype = None
        self.lib.mlx_put_pixel.argtypes = [
            ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32
        ]

        self.lib.mlx_loop.restype = None
        self.lib.mlx_loop.argtypes = [ctypes.c_void_p]

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        """Draw one pixel if it is inside the image."""
        if 0 <= x < self.win_width and 0 <= y < self.win_height:
            self.lib.mlx_put_pixel(self.img, x, y, color)

    def draw_rectangle(
        self, x1: int, y1: int, x2: int, y2: int, color: int
    ) -> None:
        """Draw and fill a rectangle."""
        if x1 > x2 or y1 > y2:
            print("Error: Invalid size.")
            sys.exit(1)

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
        """Choose fill color for one cell."""
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
        x1 = cell.col * cell_size
        y1 = cell.row * cell_size
        x2 = x1 + cell_size - 1
        y2 = y1 + cell_size - 1

        # Fill background first
        self.draw_rectangle(x1, y1, x2, y2, self.get_cell_background(cell))

        # Draw walls
        for offset in range(wall_thickness):
            if cell.has_wall(NORTH):
                self.draw_hline(x1, x2, y1 + offset, self.wall_color)
            if cell.has_wall(SOUTH):
                self.draw_hline(x1, x2, y2 - offset, self.wall_color)
            if cell.has_wall(WEST):
                self.draw_vline(x1 + offset, y1, y2, self.wall_color)
            if cell.has_wall(EAST):
                self.draw_vline(x2 - offset, y1, y2, self.wall_color)
    
    def handle_key(self):
        """Handles the key choices"""
        
        @ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
        def keys(key, param):
            if key == 256:
                print("Exit")
                sys.exit(1)
            elif key == 82:
                pass
                self.draw_maze(0, 0)
            elif key == 80:
                pass
            elif key == 67:
                pass
        
        self.key_callback = keys
        self.lib.mlx_key_hook(self.mlx, self.key_callback, None)

    def draw_maze(self, grid: list[list[Cell]]) -> None:
        """Draw the full maze grid."""
        for row in grid:
            for cell in row:
                self.draw_cell(cell)