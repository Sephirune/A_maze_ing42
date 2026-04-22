from mazegen import MazeGenerator

entry = (0, 0)
exit = (9, 9)

gen = MazeGenerator(width=10, height=10, seed=42, entry=entry, exit=exit)
maze = gen.generate()

print(maze)
