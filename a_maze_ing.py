from mlx import MlxDisplay, cell_size
import parser_conf
import ctypes
from sys import argv
from cell import Cell, NORTH, EAST, SOUTH, WEST

"""Ahora mismo 'falseamos' las celdas, esto lo tiene que hacer otra clase usando la info de config en condiciones"""
def build_initial_grid(config: parser_conf.Mazeconf) -> list[list[Cell]]:
    """Create a grid of cells with all walls closed."""
    grid: list[list[Cell]] = []

    for row in range(config.height):
        current_row: list[Cell] = []
        for col in range(config.width):
            cell = Cell(row=row, col=col)

            if (col, row) == config.entry:
                cell.is_entry = True
            if (col, row) == config.exit:
                cell.is_exit = True

            current_row.append(cell)
        grid.append(current_row)

    return grid


def main():
    config = parser_conf.validate_conf(argv[1])
    print("Config OK")
    display = MlxDisplay(config)
    print("MlxDisplay created OK")
    print(f"Drawing rectangle: 4, 5, {config.width * cell_size}, {config.height * cell_size}")
    grid = build_initial_grid(config)
    grid[4][4].remove_wall(NORTH)
    grid[4][4].remove_wall(SOUTH)
    grid[4][4].remove_wall(EAST)
    grid[4][4].remove_wall(WEST)
    grid[4][5].remove_wall(NORTH)
    grid[4][5].remove_wall(SOUTH)
    grid[4][5].remove_wall(EAST)
    grid[4][5].remove_wall(WEST)
    display.draw_maze(grid)
    print("Rectangle drawn OK")
    display.lib.mlx_loop.restype = ctypes.c_void_p
    print("Starting mlx_loop...")
    display.lib.mlx_loop(display.mlx)


main()
