*This project has been created as part of the 42 curriculum by aarogarc, guantino.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and visualizer written in Python 3.10+. The program reads a configuration file, generates a maze using a recursive backtracker (iterative DFS) algorithm, computes the shortest path from the entry to the exit using BFS, and displays the result in a graphical window powered by MLX42. The maze always contains a visible "42" pattern formed by fully blocked cells near the center.

Key features:
- Perfect maze generation (unique path between any two cells) or imperfect (with extra openings)
- Shortest path computation and visual overlay
- Embedded "42" pattern using blocked cells
- Interactive graphical display with keyboard controls
- Reproducible generation via seed
- Hex-encoded output file with entry, exit, and solution path

---

## Instructions

### Dependencies

The project requires Python 3.10 or later and the MLX42 library compiled as a shared object.

**Install Python dependencies:**
```bash
make install
```

**Compile MLX42 (requires cmake and libglfw3-dev):**
```bash
git clone https://github.com/codam-coding-college/MLX42.git
cd MLX42
mkdir build && cd build
cmake .. -DBUILD_SHARED_LIBS=ON
make -j4
cp libmlx42.so ../../lib/
```

If you do not have sudo access, compile GLFW locally first:
```bash
git clone https://github.com/glfw/glfw.git
cd glfw
cmake -S . -B build -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=$HOME/.local
cmake --build build
cmake --install build
```

Then point MLX42 to it:
```bash
cmake .. -DBUILD_SHARED_LIBS=ON -DGLFW_DIR=$HOME/.local/lib/cmake/glfw3
```

### Running the program

```bash
python3 a_maze_ing.py config.txt
```

### Makefile rules

| Rule | Description |
|---|---|
| `make install` | Install Python dependencies |
| `make run` | Run with default config.txt |
| `make debug` | Run with Python debugger (pdb) |
| `make lint` | Run flake8 and mypy with required flags |
| `make lint-strict` | Run mypy with --strict |
| `make clean` | Remove __pycache__ and .mypy_cache |

### Keyboard controls (graphical window)

| Key | Action |
|---|---|
| `R` | Re-generate a new maze |
| `P` | Show / Hide the shortest path |
| `C` | Cycle wall colours |
| `ESC` | Quit |

---

## Configuration File

The configuration file uses one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

**Mandatory keys:**

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width in cells (integer > 0) | `WIDTH=20` |
| `HEIGHT` | Maze height in cells (integer > 0) | `HEIGHT=15` |
| `ENTRY` | Entry cell coordinates as `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit cell coordinates as `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Path to the output hex file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether to generate a perfect maze | `PERFECT=True` |

**Optional keys:**

| Key | Description | Example |
|---|---|---|
| `SEED` | Integer seed for reproducibility | `SEED=42` |

**Example config.txt:**
```ini
# A-Maze-ing default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

**Notes:**
- `ENTRY` and `EXIT` must be different cells inside the maze bounds.
- If `SEED` is omitted, a random seed is generated and printed to stdout so you can reproduce the maze later.
- `PERFECT=True` guarantees exactly one path between any two cells.
- The maze must be at least 3×3. The "42" pattern requires at least 15×15.

---

## Output File Format

Each cell is encoded as one hexadecimal digit where each bit represents a wall:

| Bit | Direction |
|---|---|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A closed wall sets the bit to 1, an open wall sets it to 0. Cells are written row by row, one row per line. After an empty line, three additional lines follow: entry coordinates, exit coordinates, and the shortest path as a sequence of N/E/S/W letters.

---

## Maze Generation Algorithm

The project uses **iterative depth-first search (recursive backtracker)**.

### How it works

1. Start from the entry cell and mark it as visited.
2. Push it onto a stack.
3. While the stack is not empty, look at the top cell and pick a random unvisited, non-blocked neighbour.
4. Carve the shared wall between the two cells and mark the neighbour as visited.
5. If no unvisited neighbours exist, pop the stack and backtrack.

### Why this algorithm

Iterative DFS was chosen for three reasons. First, it produces mazes with long, winding corridors that feel natural and are satisfying to solve. Second, it is simple to implement correctly as a perfect maze generator — the result is guaranteed to be a spanning tree of the grid, meaning exactly one path exists between any two cells. Third, replacing Python's call stack with an explicit stack avoids recursion depth limits for large mazes, making it reliable regardless of maze size.

Alternatives considered were Prim's algorithm (produces mazes with shorter dead ends, less interesting visually) and Kruskal's algorithm (requires a union-find structure, more complex to implement).

### Shortest path

The solution path is computed with **BFS (breadth-first search)**, which guarantees the shortest path in an unweighted graph. The path is stored as a sequence of N/E/S/W direction letters and written to the output file.

---

## Reusable Module

The maze generation logic is packaged as a standalone pip-installable module named `mazegen-*` located at the root of the repository.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or build it yourself:
```bash
pip install build
python -m build
```

### Usage

```python
from mazegen import MazeGenerator

# Basic usage
gen = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14))
maze = gen.generate()

# With seed for reproducibility
gen = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14), seed=42)
maze = gen.generate()

# Non-perfect maze (extra openings)
gen = MazeGenerator(width=20, height=15, entry=(0, 0), exit=(19, 14), perfect=False)
maze = gen.generate()

# Access the grid (list of lists of Cell objects)
for row in maze.grid:
    for cell in row:
        print(cell.walls)  # bitmask: bit0=N, bit1=E, bit2=S, bit3=W

# Access the solution
from mazegen.solver import shortest_path
path = shortest_path(maze, entry=(0, 0), exit=(19, 14))
print(path)  # e.g. ['S', 'S', 'E', 'N', ...]
```

### API reference

| Class / Function | Description |
|---|---|
| `MazeGenerator(width, height, entry, exit, seed, perfect)` | Main generator class |
| `MazeGenerator.generate()` | Returns a `Maze` object |
| `Maze.grid` | 2D list of `Cell` objects |
| `Maze.width`, `Maze.height` | Maze dimensions |
| `Maze.entry`, `Maze.exit` | Entry and exit coordinates |
| `Cell.walls` | Bitmask of closed walls |
| `Cell.is_blocked` | True if cell is part of the "42" pattern |
| `shortest_path(maze, entry, exit)` | Returns path as list of N/E/S/W strings |

The module format (Cell bitmask) is identical to the output file format.

---

## Team and Project Management

### Roles

| Member | Responsibilities |
|---|---|
| aarogarc | Frontend: config parser, MLX42 display, keyboard interaction, menu, a_maze_ing.py |
| guantino | Backend: MazeGenerator, Maze, Cell, solver (BFS), writer, reusable package |

### Planning

The initial plan was to split the project cleanly between backend (maze logic) and frontend (display), agreeing on the `MazeGenerator` interface before starting. This worked well — both members could develop in parallel using a mock grid on the frontend side while the generator was being built.

The main deviation from the original plan was the time spent on MLX42 integration. Getting `ctypes` to correctly call MLX42 from Python required more iteration than expected, particularly around pointer return types and the keyboard hook mechanism (`mlx_key_hook` vs `mlx_loop_hook`).

### What worked well

- Defining the interface between modules early allowed true parallel development.
- Using a `@dataclass` for `Cell` kept the data model clean and easy to extend.
- The `validate_wall_consistency` check in `Maze` caught generation bugs early.
- Separating `MazeGenerator` into a pip package made the reusability requirement straightforward.

### What could be improved

- The pixel-by-pixel drawing in Python is slow for large mazes — a future improvement would be to write the rendering in C or use a faster buffer approach.
- The "42" pattern placement could be smarter — currently it is always centered, which sometimes conflicts with the entry/exit path.
- Adding multiple generation algorithms (Prim's, Kruskal's) would make the bonus more complete.

### Tools used

- **VSCode** with the Python and mypy extensions
- **flake8** and **mypy** for linting and type checking
- **pytest** for unit tests (not submitted)

---

## Resources

- [MLX42 documentation — Codam Coding College](https://github.com/codam-coding-college/MLX42)
- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python ctypes documentation](https://docs.python.org/3/library/ctypes.html)
- [PEP 557 — Data Classes](https://peps.python.org/pep-0557/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [flake8 documentation](https://flake8.pycqa.org/en/latest/)

### AI usage

| How AI was used |
| Task | How AI was used |
|---|---|
| MLX42 + ctypes integration | Understanding `restype`/`argtypes`, debugging 64-bit pointer corruption, translating the C example to Python |
| Config parser | Reviewing validation logic and identifying bugs (bounds check, `open()` path) |
| Keyboard hooks | Diagnosing why `mlx_key_hook` was not firing and switching to `mlx_loop_hook` + `mlx_is_key_down` |
| README structure | Drafting the initial structure based on subject requirements |

In all cases, AI-generated suggestions were read, understood, tested, and modified before being added to the codebase. No code was copy-pasted without full comprehension.
