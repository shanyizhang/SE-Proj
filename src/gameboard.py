## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Liu
## ----------------------------------------


class Gameboard(object):
    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.grid = self.update(occupied=None)

    def update(self, occupied: dict):
        grid = [[(0,0,0) for x in range(self.column)] for x in range(self.row)]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if occupied is not None and (j,i) in occupied:
                    c = occupied[(j,i)]
                    grid[i][j] = c
        return grid        