from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class MazeConfig:
    """Valid maze configuration"""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


def parse_coords(key: str) -> tuple[int, int]:
    """Parse x and y string intro a tuple of ints in the form 'x,y'"""

    coords = key.split(",")

    if len(coords) != 2:
        raise ValueError(f"Invalid coordinates format: {key} should be in the \
            form 'x,y'.")

    try:
        coord1 = int(coords[0].strip())
        coord2 = int(coords[1].strip())
    except ValueError as exc:
        raise ValueError(
            f"Invalid coordinates format: {key}. Coordinates must be integers."
        ) from exc

    return (coord1, coord2)


def parse_bool(value: str) -> bool:
    """Parse a strict boolean string"""
    stripped = value.strip()
    if stripped == "True":
        return True
    if stripped == "False":
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def _read_config_file(config_path: str) -> dict[str, str]:
    """Read KEY=VALUE pairs from a config file."""
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data: dict[str, str] = {}

            for raw_line in f:
                line = raw_line.strip()

                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise ValueError(f"Invalid config syntax: {line}")

                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()

                if not key:
                    raise ValueError(f"Invalid config key in line: {line}")

                data[key] = value

            return data
    except FileNotFoundError as exc:
        raise ValueError(f"Configuration file not found: {config_path}") from \
            exc


def validate_conf(config_path: str) -> MazeConfig:
    """Parse and validate the config file."""
    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    data = _read_config_file(config_path)

    missing = required_keys - data.keys()
    if missing:
        raise ValueError(f"Missing required config keys: {sorted(missing)}")

    try:
        width = int(data["WIDTH"])
        height = int(data["HEIGHT"])
    except ValueError as exc:
        raise ValueError("WIDTH and HEIGHT must be integers.") from exc

    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive integers.")

    if width < 3 or height < 3:
        raise ValueError("Maze should be at least 3x3")

    if width < 8 or height < 6:
        print("Warning: Maze should be at least 8x6 to generate 42 pattern")

    entry_coords = parse_coords(data["ENTRY"])
    exit_coords = parse_coords(data["EXIT"])

    if entry_coords == exit_coords:
        raise ValueError("ENTRY and EXIT must be different coordinates")

    if not (
        0 <= entry_coords[0] < width and 0 <= entry_coords[1] < height
    ):
        raise ValueError(f"Entry coordinates: {entry_coords} out of bounds.")

    if not (
        0 <= exit_coords[0] < width and 0 <= exit_coords[1] < height
    ):
        raise ValueError(f"Exit coordinates: {exit_coords} out of bounds.")

    output_file = data["OUTPUT_FILE"].strip()
    if not output_file:
        raise ValueError("OUTPUT_FILE must not be empty.")

    perfect = parse_bool(data["PERFECT"])

    seed: Optional[int] = None
    if "SEED" in data:
        try:
            seed = int(data["SEED"])
        except ValueError as exc:
            raise ValueError("SEED must be an integer.") from exc
    else:
        seed = random.randint(0, 2**32 - 1)

    random.seed(seed)

    return MazeConfig(
        width=width,
        height=height,
        entry=entry_coords,
        exit=exit_coords,
        output_file=data["OUTPUT_FILE"],
        perfect=perfect,
        seed=seed
    )
