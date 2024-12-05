from tkinter import Tk, BOTH, Canvas
import time
import random

class Window():
    def __init__(self, width, height, bg = "gray70"):
        self._bg = bg
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg=bg, height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

#drawing logic
    def draw_line(self, line, color):
        line.draw(self.__canvas, color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
#closing logic
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        self.__root.destroy() #stop lingering window when a new instance is opened in quick aftr closing

    def close(self):
        self.__running = False
    

class Pixel():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        #print("Printing pixel")
        #print(f"I'm a pixel at (x,y) {self.x, self.y}")
        return f"Pixel {self.x, self.y}"

class Line():
    def __init__(self, B, E):
        self.b = B
        self.e = E
    
    def draw(self, canvas, color):
        canvas.create_line(self.b.x, self.b.y, self.e.x, self.e.y, fill=color, width=2)
    
    def __str__(self):
        #print ("Printing Line")
        #print(f"I'm a line between point A {self.pointA} and point B {self.pointB}")
       return f"Line between {self.b} and {self.e}"

class Cell():
    def __init__(self, x, y, window=None, width=50, height=50): #coordinates of top-left corner
        self.height = height
        self.width = width
        self.has_left = True
        self.has_right = True
        self.has_top = True
        self.has_bottom = True
        self._x1 = x
        self._y1 = y
        self._x2 = x + self.width
        self._y2 = y + self.height
        self._win = window
        self.visited = False

    def draw(self, color = "black", noise = False):
        if self._win == None:
            return
        bg = self._win._bg
        #print("Drawing Cell")
        ln_left = Line(Pixel(self._x1, self._y1),Pixel(self._x1, self._y2))
        ln_right = Line(Pixel(self._x2, self._y1),Pixel(self._x2, self._y2))
        ln_top = Line(Pixel(self._x1, self._y1),Pixel(self._x2, self._y1))
        ln_bottom = Line(Pixel(self._x1, self._y2),Pixel(self._x2, self._y2))
        if self.has_left:
            self._win.draw_line(ln_left, color)
        else:
            self._win.draw_line(ln_left, bg)

        if self.has_right:
            self._win.draw_line(ln_right, color)
        else:
            self._win.draw_line(ln_right, bg)

        if self.has_top:
            self._win.draw_line(ln_top, color)
        else:
            self._win.draw_line(ln_top, bg)
            
        if self.has_bottom:
            self._win.draw_line(ln_bottom, color)
        else:
            self._win.draw_line(ln_bottom, bg)   
        
        if noise:
            print (f"Drawing {self}")
    
    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "red"
        else:
            color = "lime"

        path = Line(self._get_center(), to_cell._get_center())
        #print("Drawing path", path, "in", color)
        self._win.draw_line(path, color)
    
    def _break_wall(self, direction):
        #all walls
        match direction:
            case "bottom":
                self.has_bottom = False
            case "top":
                self.has_top = False
            case "left":
                self.has_left = False
            case "right":
                self.has_right = False
            case _:
                raise Exception(f"invalid direction |{direction}|, accepts only  top, bottom, left or right")
        if self._win == None: #can only draw lines when you have a canvas
            return
        self.draw()
    
    def _debug_wall_status(self):
        Walls = []
        if self.has_left:
            Walls.append("Left")
        if self.has_right:
            Walls.append("Right")
        if self.has_top:
            Walls.append("Top")
        if self.has_bottom:
            Walls.append("Bottom") 
        return Walls

    def _get_center(self):
        return Pixel(self._x1 + int(self.width/2), self._y1 + int(self.height/2))

    def __str__(self):
        Walls = []
        if self.has_left:
            Walls.append("Left")
        if self.has_right:
            Walls.append("Right")
        if self.has_top:
            Walls.append("Top")
        if self.has_bottom:
            Walls.append("Bottom") 
        return f"Cell (r{int(self._x1/self.width)+1}, c{int(self._y1/self.height+1)}) with walls {Walls}" 

    def __repr__(self):
        Walls = []
        if self.has_left:
            Walls.append("Left")
        if self.has_right:
            Walls.append("Right")
        if self.has_top:
            Walls.append("Top")
        if self.has_bottom:
            Walls.append("Bottom") 
        return f"{self._x1, self._x2} Walls: {Walls}"

#Maze is now it's own file because it got a bit long