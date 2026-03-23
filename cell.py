walls = {
    "north": 0b0001,
    "east": 0b0010,
    "south": 0b0100,
    "west": 0b1000
}


class Cell():
    def __init__(self, row: int, col: int, walls: int = 0b1111) -> None:
        self.row = row
        self.col = col
        self.walls = walls
        self.visited = False
        self.is_entry = False
        self.is_exit = False
        self.is_path = False
        self.is_bloqued = False

    def has_wall(self, dir):
        return (self.walls & walls[dir] == 1)
    
    def remove_wall(self, dir):
        self.walls = self.walls & ~walls[dir]

    def add_wall(self, dir):
        self.walls = self.walls | dir