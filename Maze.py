from classes import *

class Maze():
    def __init__(self,x1,y1,num_rows,num_cols,cell_size_x,cell_size_y,win=None, seed = None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols    
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._seed = seed
        if seed:
            random.seed(seed)  

        self._create_cells()
        self._reset_cells_visited()
        #self._redraw_maze()
         
    def _create_cells(self):
        if (self._num_rows <= 0 or self._num_cols <=0):
            self._cells = [[]]
            return

        for r in range(self._num_rows):
            self._cells.append([])
            for c in range(self._num_cols):
                x = self._x1 + c*self._cell_size_x
                y = self._y1 + r*self._cell_size_y
                self._cells[r].append(Cell(x, y, self._win, self._cell_size_x, self._cell_size_y))
                if self._win != None:
                    self._draw_cell(r,c)

        self._break_entrance_and_exit()
        self._break_walls(0,0)
        #print ("\nDEBUG created Labyrinth with these cells:", self._cells, f"\nat ({self._x1},{self._y1})\n")
        if self._win != None:
            self._animate()
        
        
    def _draw_cell(self, r, c):
        #__init__(self, x, y, window, height=50, width=50)
        #print(r,x, "|", c, y)
        self._cells[r][c].draw(noise=False)
        self._animate()
        
    def _animate(self, drawtime=0.01):
        if self._num_rows * self._num_cols < 17:
            drawtime += 0.04
        self._win.redraw()
        time.sleep(drawtime)
    
    def _break_entrance_and_exit(self):
        if self._cells == [[]]: #empty maze
            return
        #entrance top at top-left cell
        row = 0
        col = 0
        self._cells[row][col]._break_wall("top")
        #exit bottom at bottom-right-cell
        row = len(self._cells)-1
        col = len(self._cells[0])-1
        self._cells[row][col]._break_wall("bottom")
        #if row < 3:
        #    print("DEBUG after creating e and e", self._cells, "\n")
    
    def _break_walls(self, r, c):
        self._cells[r][c].visited = True
        i = 0
        while True:
            to_visit = []
            #check top
            if r > 0:
                if not self._cells[r-1][c].visited:
                    to_visit.append((r-1,c,"top", "bottom"))
            #check bottom   
            if r < self._num_rows-1:
                if not self._cells[r+1][c].visited:
                    to_visit.append((r+1,c,"bottom", "top"))
            #check left
            if c > 0:
                if not self._cells[r][c-1].visited:
                    to_visit.append((r,c-1, "left", "right"))
            #check right
            if c < self._num_cols-1:
                if not self._cells[r][c+1].visited:
                    to_visit.append((r,c+1, "right", "left"))

            #print(f"self: {self._cells[r][c]}, potential new breaks: {to_visit}")
            if to_visit == []:
                #print (f"\n----no new neighbors for {self._cells[r][c]}, backtrack")
                #self._cells[r][c].draw() #draws when breaking wall
                return

            choice = to_visit.pop(random.randrange(0,len(to_visit)))
            #print (f"self: {self._cells[r][c]} neighbor: {self._cells[choice[0]][choice[1]]}")

            #break own wall
            #print (f"\nbreaking |{choice[2]}| wall of {self._cells[r][c]}")
            self._cells[r][c]._break_wall(choice[2])
            #print ("new status self:", self._cells[r][c])
            #break neighbor wall
            #print (f"breaking |{choice[3]}| wall of neighbor {self._cells[choice[0]][choice[1]]}")
            self._cells[choice[0]][choice[1]]._break_wall(choice[3])
            #print ("new status neighbor:", self._cells[choice[0]][choice[1]])
            #recursive call
            self._break_walls(choice[0],choice[1])
    
    def _reset_cells_visited(self):
        #print("Resetting visited status")
        for r in range(self._num_rows):
            for c in range(self._num_cols):
                self._cells[r][c].visited = False
      
    def _debug_status_cells_visited(self):
        all_cells = []
        not_visited = []
        for r in range(self._num_rows):
            for c in range(self._num_cols):
                all_cells.append((r,c, self._cells[r][c].visited))
                if self._cells[r][c].visited == False:
                    not_visited.append((r,c, ))

        print (f"DEBUG status of all cells: {all_cells}")
        print (f"DEBUG not visited cells: {not_visited}")
    
    def _debug_status_maze(self):
        print ("Maze rows should be", self._num_rows, "it has", len(self._cells))
        print ("Maze columns should be", self._num_cols, "it has", len(self._cells[0]))

        print ("The maze contains these cells:")
        for r in range(self._num_rows):
            for c in range(self._num_cols):
                print(self._cells[r][c])

    def solve(self, smart = False):
        if self._cells == [[]]:
            raise Exception ("A maze that doesn't exist can not be solved!")
        
        print("Stating to solve")
        success = self._solve_r(0,0, smart)
        if success:
            print("Found the path!")
        else:
            print("failed to find a path")
    
    def _solve_r(self, r, c, smart = False):
        if smart:
            return self._solve_smart(r,c)

        self._animate(0.05)
        self._cells[r][c].visited = True
        if r == self._num_rows -1 and c == self._num_cols-1:
            #is the end cell, the maze is solved
            return True

        to_try = []
        act = self._cells[r][c]
        if r < self._num_rows-1  and not act.has_bottom:
            if not self._cells[r+1][c].visited:
                to_try.append((r+1, c))    
        if c < self._num_cols-1  and not act.has_right:
            if not self._cells[r][c+1].visited:
                to_try.append((r,c+1))  
        if r > 0  and not act.has_top:
            if not self._cells[r-1][c].visited:
                to_try.append((r-1,c))
                to_try.append((r-1,c))
        if c > 0  and not act.has_left:
            if not self._cells[r][c-1].visited:
                to_try.append((r,c-1))
  

        #choose
        if to_try == []:
            #dead end
            return False

        random.shuffle(to_try)

        for ch in to_try:
            #print ("ch", ch, type(ch))
            #draw move
            self._cells[r][c].draw_move(self._cells[ch[0]][ch[1]])
            solved = self._solve_r(ch[0],ch[1])
            if solved:
                return True
            else:
                self._cells[r][c].draw_move(self._cells[ch[0]][ch[1]],True)
        return False

    def _solve_smart(self, r,c):
        print ("The smarter solving algorith doesn't exist yet. Will proceed to use the other one instead.")
        return self._solve_r(r,c)
            