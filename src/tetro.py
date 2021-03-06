## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import random
from enum import Enum


S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]

COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class TetroState(Enum):
    Alive = "Alive"
    Dead = "Dead"


class Tetromino(object):
    def __init__(self, x: int, y: int, t_index: int):
        """
        Init the Tetromino
        Input: Coordinates and index
        Output: None
        """
        self.x = x
        self.y = y
        self.shape = SHAPES[t_index]
        self.color = COLORS[t_index]
        self.rotation = 0
        self.state = TetroState.Alive

    def down(self):
        """ Move Downward """
        self.y += 1
    
    def up(self):
        """ Move Upward """
        self.y -= 1

    def left(self):
        """ Move Left """
        self.x -= 1

    def right(self):
        """ Move Right """
        self.x += 1

    def rotate_clockwise(self):
        """ Rotate Clockwise """
        self.rotation = (self.rotation + 1) % len(self.shape)

    def rotate_counterclockwise(self):
        """ Rotate CounterClockwise """
        self.rotation = (self.rotation - 1) % len(self.shape)

    def die(self):
        """ Tetromino hits the bottom """
        self.state = TetroState.Dead
    
    def check_die(self):
        """ Check if the Tetromino dies """
        return self.state == TetroState.Dead


class TetrominoProxy(object):
    def __init__(self, column):
        """
        Init the TetrominoProxy
        Input: Number of columns
        Output: None
        """
        self.column = column
        self.tetromino_array = [self.generate()]

    def generate(self, index=None, blacklist=None):
        """ Generate a new Tetromino """
        if index is None and blacklist is None:
            return Tetromino(x=self.column/2, y=0, t_index=random.randint(0, len(SHAPES)-1))
        if index is not None:
            return Tetromino(x=self.column/2, y=0, t_index=index)
        if blacklist is not None:
            if len(blacklist) < len(SHAPES):
                while True:
                    index = random.randint(0, len(SHAPES)-1)
                    if index not in blacklist:
                        return Tetromino(x=self.column/2, y=0, t_index=index)
            else:
                return Tetromino(x=self.column/2, y=0, t_index=random.randint(0, len(SHAPES)-1))

    def dump_next(self, index_next=None, blacklist_next=None):
        """ Output the Tetromino in the buffer """
        self.tetromino_array.append(self.generate(index=index_next, blacklist=blacklist_next))
        return self.tetromino_array.pop(0)
        
    def view_next(self):
        """ Take a glance at the next Tetromino """
        return self.tetromino_array[0]

    @staticmethod
    def convert_shape_format(shape):
        """
        Convert the shape representation of the Tetromino
        Input: Input shape
        Output: Converted shape
        """
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
        for i, pos in enumerate(positions):
            positions[i] = (int(pos[0] - 2), int(pos[1] - 4))
        return positions