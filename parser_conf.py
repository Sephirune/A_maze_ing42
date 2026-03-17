import sys
from dataclasses import dataclass  # básicamente sirve para construir una clase de datos
from typing import Optional
import random


@dataclass
class Mazeconf:
    """Valid maze configuration"""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


def parse_coords(key: str) -> tuple[int, int]:
    """Parse x and y string intro a tuple of ints"""

    coords = key.split(",")

    if len(coords) != 2:
        raise ValueError("Invalid entry format")

    try:
        coord1 = coords[0].strip()
        coord2 = coords[1].strip()
        return (int(coord1), int(coord2))
    except ValueError:
        raise ValueError(f"Invalid entry format: {key}. Entry must be int.")


def parse_bool(value: str) -> bool:
    """Parse 'True' or 'False' string into bool"""

    if value.strip() == "True":
        return True
    elif value.strip() == "False":
        return False
    else:
        raise ValueError("Invalid boolean.")


def validate_conf(config_path: str) -> Mazeconf:
    """Parse and validate configuration.txt"""

    required_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                     "PERFECT"}

    try:
        with open("config.txt", "r") as f:
            sanitized: dict[str, str] = {}
            for line in f:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise ValueError("Invalid config syntax.")
                key, sign, values = line.partition("=") # Partition devuelve una tupla con 3 elementos: antes del objetivo, la palabra a buscar, y lo siguiente.
                sanitized[key.strip()] = values.strip()
    except FileNotFoundError:
        print("config.txt not found. Error reading file")
        sys.exit(1)

    difference = required_keys - sanitized.keys()  # Comparo con las keys del dict
    if difference:
        raise ValueError("Missing keys required.")

    try:
        width = int(sanitized["WIDTH"])
        height = int(sanitized["HEIGHT"])
        if width <= 0 or height <= 0:
            raise ValueError("WIDTH and HEIGHT must be positive integers")

        entry_coords = parse_coords(sanitized["ENTRY"])
        exit_coords = parse_coords(sanitized["EXIT"])

        if entry_coords == exit_coords:
            raise ValueError("ENTRY and EXIT must be different coordinates")
        if (entry_coords[0] < 0 or entry_coords[0] < width or entry_coords[1]< 0 or entry_coords[1] < width):
            raise ValueError(f"Entry coordinates: {entry_coords} not valid.")
        if (exit_coords[0] < 0 or exit_coords[0] < height or exit_coords[1] < 0 or exit_coords[1] < height):
            raise ValueError(f"Entry coordinates: {exit_coords} not valid.")
        if width < 3 or height < 3:
            raise ValueError("Maze should be at least 3x3")
        if width < 8 or height < 6:
            print("Maze should be at least 8x6 to generate 42")

        seed: Optional[int] = None
        if "SEED" in sanitized:
            try:
                seed = int(sanitized["SEED"])
            except ValueError:
                raise ValueError("SEED must be an integer.")
        else:
            seed = random.randint(0, 2**32 - 1) # Esta fórmula es por convenio para representar números sin signo en 32 bits.

        perfect = parse_bool(sanitized["PERFECT"])

        return Mazeconf(
            width=width,
            height=height,
            entry=entry_coords,
            exit=exit_coords,
            output_file=sanitized["OUTPUT_FILE"],
            perfect=perfect,
            seed=seed
        )
    except ValueError as e:
        raise ValueError(f"Invalid configuration file: {e}")
