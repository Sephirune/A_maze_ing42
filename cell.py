from __future__ import annotations

from dataclasses import dataclass

NORTH: int = 0b0001
EAST: int = 0b0010
SOUTH: int = 0b0100
WEST: int = 0b1000
ALL_WALLS: int = NORTH | EAST | SOUTH | WEST

DIRECTION_OFFSETS: dict[int, tuple[int, int]] = {
    NORTH: (-1, 0),
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1),
}

OPPOSITE_WALL: dict[int, int] = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}

DIRECTION_LETTERS: dict[int, str] = {
    NORTH: "N",
    EAST: "E",
    SOUTH: "S",
    WEST: "W",
}

LETTER_TO_DIRECTION: dict[str, int] = {
    "N": NORTH,
    "E": EAST,
    "S": SOUTH,
    "W": WEST,
}


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
    visited: bool = False

    def has_wall(self, direction: int) -> bool:
        """Return True if the given wall exists."""
        return (self.walls & direction) != 0

    def remove_wall(self, direction: int) -> None:
        """Remove one wall."""
        self.walls &= ~direction

    def add_wall(self, direction: int) -> None:
        """Add one wall."""
        self.walls |= direction

    def reset_visual_flags(self) -> None:
        """Clear non-structural display flags."""
        self.is_path = False