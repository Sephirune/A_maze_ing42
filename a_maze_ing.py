from mlx import MlxDisplay, cell_size
import parser_conf
import ctypes
from sys import argv
from cell import Cell, NORTH, EAST, SOUTH, WEST
from mazegen import build_initial_grid


def main():
    config = parser_conf.validate_conf(argv[1])
    print("Config OK")
    display = MlxDisplay(config)
    print("MlxDisplay created OK")
    print(f"Drawing rectangle: 4, 5, {config.width * cell_size}, {config.height * cell_size}")
    grid = build_initial_grid(config)
    display.draw_maze(grid)
    print("Rectangle drawn OK")
    display.lib.mlx_loop.restype = ctypes.c_void_p
    print("Starting mlx_loop...")
    display.lib.mlx_loop(display.mlx)


main()
