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
        self.x = x
        self.y = y
        self.shape = SHAPES[t_index]
        self.color = COLORS[t_index]
        self.rotation = 0
        self.state = TetroState.Alive

    def down(self):
        self.y += 1
    
    def up(self):
        self.y -= 1

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def rotate_clockwise(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    def rotate_counterclockwise(self):
        self.rotation = (self.rotation - 1) % len(self.shape)

    def die(self):
        self.state = TetroState.Dead
    
    def check_die(self):
        return self.state == TetroState.Dead


class TetrominoProxy(object):
    def __init__(self, column):
        self.column = column
        self.tetromino_array = [self.generate()]

    def generate(self, index=None):
        if index is None:
            return Tetromino(x=self.column/2, y=0, t_index=random.randint(0, len(SHAPES)-1))
        else:
            return Tetromino(x=self.column/2, y=0, t_index=index)

    def dump_next(self, index_next=None):
        self.tetromino_array.append(self.generate(index=index_next))
        return self.tetromino_array.pop(0)
        
    def view_next(self):
        return self.tetromino_array[0]

    @staticmethod
    def convert_shape_format(shape):
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