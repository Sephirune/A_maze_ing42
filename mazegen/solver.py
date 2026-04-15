from __future__ import annotations

from collections import deque

from .cell import DIRECTION_LETTERS, DIRECTION_OFFSETS, LETTER_TO_DIRECTION
from .maze import Maze


def shortest_path(
    maze: Maze,
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> list[str]:
    """Return the shortest path from entry to exit as N/E/S/W letters."""
    start = (entry[1], entry[0])
    goal = (exit[1], exit[0])

    queue: deque[tuple[int, int]] = deque([start])
    parents: dict[tuple[int, int], tuple[tuple[int, int], int] | None] = {
        start: None
    }

    while queue:
        row, col = queue.popleft()

        if (row, col) == goal:
            break

        cell = maze.cell_at(row, col)

        for direction, (drow, dcol) in DIRECTION_OFFSETS.items():
            if cell.has_wall(direction):
                continue

            nrow = row + drow
            ncol = col + dcol

            if not maze.in_bounds(nrow, ncol):
                continue

            neighbor = maze.cell_at(nrow, ncol)
            if neighbor.is_blocked:
                continue

            if (nrow, ncol) in parents:
                continue

            parents[(nrow, ncol)] = ((row, col), direction)
            queue.append((nrow, ncol))

    if goal not in parents:
        raise ValueError("No valid path found from entry to exit.")

    path_dirs: list[str] = []
    current = goal

    while True:
        entry_data = parents[current]
        if entry_data is None:
            break
        previous, direction = entry_data
        path_dirs.append(DIRECTION_LETTERS[direction])
        current = previous

    path_dirs.reverse()
    return path_dirs


def mark_path(maze: Maze,
              entry: tuple[int, int],
              path_dirs: list[str]
              ) -> None:
    """Mark the cells belonging to the path."""
    maze.reset_search_flags()

    row = entry[1]
    col = entry[0]

    maze.cell_at(row, col).is_path = True

    for step in path_dirs:
        direction = LETTER_TO_DIRECTION[step]
        drow, dcol = DIRECTION_OFFSETS[direction]
        row += drow
        col += dcol
        maze.cell_at(row, col).is_path = True
