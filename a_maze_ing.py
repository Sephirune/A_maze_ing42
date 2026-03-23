from mlx import MlxDisplay
import parser_conf
from sys import argv

def main():
    
    config = parser_conf.validate_conf(argv[1])
    display = MlxDisplay(config)
    display.draw_rectangle(4, 5, config.width, config.height, 0xFFFFFFFF)

main()