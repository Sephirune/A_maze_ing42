from __future__ import annotations

import sys

from config import validate_conf
from generator import MazeGenerator
from mlx_display import MlxDisplay
from solver import mark_path, shortest_path
from writer import write_output_file


def main() -> int:
    """Run the maze generator application."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return 1

    try:
        config = validate_conf(sys.argv[1])
        print("Config OK")

        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
            seed=config.seed,
            perfect=config.perfect,
        )
        maze = generator.generate()

        path_dirs: list[str] = shortest_path(maze, config.entry, config.exit)
        mark_path(maze, config.entry, path_dirs)

        write_output_file(
            output_file=config.output_file,
            maze=maze,
            entry=config.entry,
            exit=config.exit,
            path_dirs=path_dirs,
        )

        display: MlxDisplay = MlxDisplay(
            maze=maze,
            entry=config.entry,
            exit=config.exit,
            seed=config.seed,
            perfect=config.perfect,
        )
        print("MlxDisplay created OK")
        print("Starting mlx_loop...")
        display.run()
        return 0

    except ValueError as exc:
        print(f"Error: {exc}")
        return 1
    except OSError as exc:
        print(f"System error: {exc}")
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
