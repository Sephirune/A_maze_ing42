from __future__ import annotations

import random

from cell import ALL_WALLS
from maze import Maze


class MazeGenerator:
    """Reusable maze generator."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int | None = None,
        perfect: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        self.random = random.Random(seed)

    def generate(self) -> Maze:
        """Generate and return a maze."""
        maze = Maze.create(
            width=self.width,
            height=self.height,
            entry=self.entry,
            exit=self.exit,
        )

        if self._can_place_42():
            self._place_42_pattern(maze)
        else:
            print("Warning: maze too small to place a visible '42' pattern.")

        self._generate_perfect_maze(maze)

        if not self.perfect:
            self._add_extra_openings(maze)

        maze.seal_blocked_cells()

        if not maze.validate_wall_consistency():
            raise ValueError("Generated maze has inconsistent shared walls.")

        return maze

    def _can_place_42(self) -> bool:
        """Return True if the maze is big enough for a simple 42 pattern."""
        return self.width >= 15 and self.height >= 15

    def _place_42_pattern(self, maze: Maze) -> None:
        """Place a simple blocked-cell '42' pattern near the center."""
        pattern = [
            "10010011111",
            "10010000001",
            "10010000001",
            "11110011111",
            "00010010000",
            "00010010000",
            "00010011111",
        ]

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        start_row = max(0, (maze.height - pattern_height) // 2)
        start_col = max(0, (maze.width - pattern_width) // 2)

        for prow, pattern_row in enumerate(pattern):
            for pcol, value in enumerate(pattern_row):
                if value != "1":
                    continue

                row = start_row + prow
                col = start_col + pcol

                if not maze.in_bounds(row, col):
                    continue

                if (col, row) == maze.entry or (col, row) == maze.exit:
                    continue

                cell = maze.cell_at(row, col)
                cell.is_blocked = True
                cell.walls = ALL_WALLS

    def _generate_perfect_maze(self, maze: Maze) -> None:
        """Generate a perfect maze using iterative DFS."""
        start_row = self.entry[1]
        start_col = self.entry[0]

        if maze.cell_at(start_row, start_col).is_blocked:
            raise ValueError("Entry cell cannot be blocked.")

        stack: list[tuple[int, int]] = [(start_row, start_col)]
        maze.cell_at(start_row, start_col).visited = True

        while stack:
            row, col = stack[-1]

            unvisited_neighbors: list[tuple[int, int, int]] = []
            for direction, nrow, ncol in maze.neighbors(row, col):
                neighbor = maze.cell_at(nrow, ncol)
                if neighbor.is_blocked:
                    continue
                if neighbor.visited:
                    continue
                unvisited_neighbors.append((direction, nrow, ncol))

            if not unvisited_neighbors:
                stack.pop()
                continue

            direction, nrow, ncol = self.random.choice(unvisited_neighbors)
            maze.carve_passage(row, col, direction, nrow, ncol)
            maze.cell_at(nrow, ncol).visited = True
            stack.append((nrow, ncol))

        maze.reset_search_flags()

    def _add_extra_openings(self, maze: Maze) -> None:
        """Add a few random extra openings for non-perfect mazes."""
        candidates: list[tuple[int, int, int, int, int]] = []

        for row in range(maze.height):
            for col in range(maze.width):
                cell = maze.cell_at(row, col)
                if cell.is_blocked:
                    continue

                for direction, nrow, ncol in maze.neighbors(row, col):
                    if direction not in (2, 1):
                        continue
                    neighbor = maze.cell_at(nrow, ncol)
                    if neighbor.is_blocked:
                        continue
                    if cell.has_wall(direction):
                        candidates.append((row, col, direction, nrow, ncol))

        self.random.shuffle(candidates)
        openings = max(1, (maze.width * maze.height) // 20)

        count = 0
        for row, col, direction, nrow, ncol in candidates:
            maze.carve_passage(row, col, direction, nrow, ncol)
            count += 1
            if count >= openings:
                break
