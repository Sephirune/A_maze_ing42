from mlx import MlxDisplay, cell_size
import parser_conf
import ctypes
from sys import argv

def main():
    config = parser_conf.validate_conf(argv[1])
    print("Config OK")
    
    display = MlxDisplay(config)
    print("MlxDisplay created OK")
    
    print(f"Drawing rectangle: 4, 5, {config.width * cell_size}, {config.height * cell_size}")
    display.draw_rectangle(4, 5, config.width * cell_size, config.height * cell_size, 0xFFFFFFFF)
    print("Rectangle drawn OK")
    
    display.lib.mlx_loop.restype = ctypes.c_void_p
    print("Starting mlx_loop...")
    display.lib.mlx_loop(display.mlx)

main()