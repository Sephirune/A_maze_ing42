import parser_conf
from cell import Cell


class MazeGen():
    def __init__(self, config: parser_conf.Mazeconf):
        self.config = config
        self.grid = self.build_initial_grid(config)

    def build_initial_grid(config: parser_conf.Mazeconf) -> list[list[Cell]]:
        """Create a grid of cells with all walls closed."""
        grid: list[list[Cell]] = []

        for row in range(config.height):
            current_row: list[Cell] = []
            for col in range(config.width):
                cell = Cell(row=row, col=col)

                if (col, row) == config.entry:
                    cell.is_entry = True
                if (col, row) == config.exit:
                    cell.is_exit = True

                current_row.append(cell)
            grid.append(current_row)

        return grid