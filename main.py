from constants import *
from classes import Window
from Maze import Maze
import random

#def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,win=None, seed = None):
def main():
    maze_rows = random.randrange(1,15)
    maze_cols = random.randrange(1,15)
    seed = None
    smart = False

    wnd = Window(window_width, window_height)
    maze_x = 5
    maze_y = 5
    cell_height = 50
    cell_width = 50

    new_maze = Maze(maze_x, maze_y, maze_rows, maze_cols, cell_height, cell_width, wnd, seed)
    new_maze.solve(smart)
    wnd.wait_for_close()

main()