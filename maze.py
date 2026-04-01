from __future__ import annotations

from dataclasses import dataclass

from cell import ALL_WALLS, Cell, DIRECTION_OFFSETS, OPPOSITE_WALL


@dataclass
class Maze:
    """Maze structure and helpers."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    grid: list[list[Cell]]

    @classmethod
    def create(
        cls,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> "Maze":
        """Create a maze with every cell initially fully closed."""
        grid: list[list[Cell]] = []

        for row in range(height):
            current_row: list[Cell] = []
            for col in range(width):
                cell = Cell(row=row, col=col)

                if (col, row) == entry:
                    cell.is_entry = True
                if (col, row) == exit:
                    cell.is_exit = True

                current_row.append(cell)
            grid.append(current_row)

        return cls(width=width, height=height, entry=entry, exit=exit, grid=grid)

    def in_bounds(self, row: int, col: int) -> bool:
        """Return True if the given row and col are inside the maze."""
        return 0 <= row < self.height and 0 <= col < self.width

    def cell_at(self, row: int, col: int) -> Cell:
        """Return the cell at row and col."""
        return self.grid[row][col]

    def neighbors(self, row: int, col: int) -> list[tuple[int, int, int]]:
        """Return neighbors as (direction, nrow, ncol)."""
        result: list[tuple[int, int, int]] = []

        for direction, (drow, dcol) in DIRECTION_OFFSETS.items():
            nrow = row + drow
            ncol = col + dcol
            if self.in_bounds(nrow, ncol):
                result.append((direction, nrow, ncol))

        return result

    def carve_passage(
        self,
        row: int,
        col: int,
        direction: int,
        nrow: int,
        ncol: int,
    ) -> None:
        """Open the shared wall between two adjacent cells."""
        current = self.cell_at(row, col)
        neighbor = self.cell_at(nrow, ncol)

        current.remove_wall(direction)
        neighbor.remove_wall(OPPOSITE_WALL[direction])

    def reset_search_flags(self) -> None:
        """Reset search and visual helper flags."""
        for row in self.grid:
            for cell in row:
                cell.visited = False
                cell.is_path = False

    def validate_wall_consistency(self) -> bool:
        """Ensure adjacent cells agree on shared walls."""
        for row in range(self.height):
            for col in range(self.width):
                cell = self.cell_at(row, col)

                for direction, nrow, ncol in self.neighbors(row, col):
                    neighbor = self.cell_at(nrow, ncol)
                    if cell.has_wall(direction) != neighbor.has_wall(
                        OPPOSITE_WALL[direction]
                    ):
                        return False
        return True

    def seal_blocked_cells(self) -> None:
        """Ensure blocked cells remain fully closed."""
        for row in self.grid:
            for cell in row:
                if cell.is_blocked:
                    cell.walls = ALL_WALLS