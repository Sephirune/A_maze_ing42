from dataclasses import dataclass

NORTH: int = 0b0001
EAST: int = 0b0010
SOUTH: int = 0b0100
WEST: int = 0b1000
ALL_WALLS: int = NORTH | EAST | SOUTH | WEST


@dataclass
class Cell:
    """Single maze cell."""

    row: int
    col: int
    walls: int = ALL_WALLS
    is_entry: bool = False
    is_exit: bool = False
    is_path: bool = False
    is_blocked: bool = False

    def has_wall(self, direction: int) -> bool:
        """Return True if the wall exists."""
        return (self.walls & direction) != 0

    def remove_wall(self, direction: int) -> None:
        """Open one wall."""
        self.walls &= ~direction

    def add_wall(self, direction: int) -> None:
        """Close one wall."""
        self.walls |= direction
