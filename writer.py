from __future__ import annotations

from cell import Cell
from maze import Maze


def cell_to_hex(cell: Cell) -> str:
    """Convert one cell wall bitmask to a hexadecimal digit."""
    return format(cell.walls, "X")


def write_output_file(
    output_file: str,
    maze: Maze,
    entry: tuple[int, int],
    exit: tuple[int, int],
    path_dirs: list[str],
) -> None:
    """Write the maze in the required output format."""
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            for row in maze.grid:
                line = "".join(cell_to_hex(cell) for cell in row)
                file.write(line + "\n")

            file.write("\n")
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(f"{exit[0]},{exit[1]}\n")
            file.write("".join(path_dirs) + "\n")
    except OSError as exc:
        raise ValueError(f"Failed to write output file '{output_file}': {exc}") from exc