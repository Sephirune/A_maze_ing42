import sys
from typing import Optional

class Mazeconf:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


def parse_coords(key: str) -> tuple[int, int]:
    coords = key.split(",")

    if len(coords) != 2:
        raise ValueError("Invalid entry format")

    try:
        coord1 = coords[0].strip()
        coord2 = coords[1].strip()
        return (int(coord1), int(coord2))
    except ValueError:
        raise ValueError(f"Invalid entry format: {key}. Entry must be int.")


def validate_conf(values: dict[str, str]) -> Mazeconf:
    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                     "PERFECT"}

    difference = required_keys - values
    if difference:
        raise ValueError("Missing keys required.")

    try:
        width = int(values["WIDTH"])
        height = int(values["HEIGHT"])
    except ValueError:
        raise ValueError("WIDTH and Height must be positive integers")
