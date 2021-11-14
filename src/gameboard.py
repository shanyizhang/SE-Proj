## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import pygame
from tetro import Tetromino, TetrominoProxy
from display import *

FALL_SPEED_CANDIDATE = [0.6, 0.3, 0.1]

class Gameboard(object):
    def __init__(self, column, row, tetro_proxy, diff):
        self.column = column
        self.row = row
        self.tetro_proxy : TetrominoProxy = tetro_proxy
        self.clock = pygame.time.Clock()
        
        self.fall_speed = FALL_SPEED_CANDIDATE[diff]

        self.grid = None
        self.occupied_positions = None
        self.curr_tetro : Tetromino = None
        self.fall_time = None
        self.score = None

    def update_grid(self):
        grid = [[(0,0,0) for x in range(self.column)] for x in range(self.row)]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in self.occupied_positions:
                    c = self.occupied_positions[(j,i)]
                    grid[i][j] = c
        return grid        

    def valid_space(self):
        accepted_positions = [[(j, i) for j in range(self.column) if self.grid[i][j] == (0,0,0)] for i in range(self.row)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = self.tetro_proxy.convert_shape_format(self.curr_tetro)
        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False
        return True

    @staticmethod
    def compute_score(num_inc):
        """
        compute the score when rows are cleared
        num_inc: number of rows being cleared (between 1 to 4)
        """
        if num_inc == 1:
            return 10
        elif num_inc == 2:
            return 30
        elif num_inc == 3:
            return 60
        elif num_inc == 4:
            return 100
        else:
            raise ValueError(num_inc)

    def eliminate_row(self):
        inc = 0
        for i in range(len(self.grid)-1,-1,-1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del self.occupied_positions[(j, i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(self.occupied_positions), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    self.occupied_positions[newKey] = self.occupied_positions.pop(key)
        return inc  # return number of rows eliminated

    def fail(self):
        for pos in self.occupied_positions:
            _, y = pos
            if y < 1:
                return True
        return False

    def move_downwards(self):
        self.fall_time += self.clock.get_rawtime()
        if self.fall_time/1000 >= self.fall_speed:
            self.fall_time = 0
            self.curr_tetro.down()
            if not self.valid_space() and self.curr_tetro.y > 0:
                self.curr_tetro.up()
                self.curr_tetro.die()

    def reset(self):
        self.occupied_positions = dict()
        self.grid = self.update_grid()
        self.curr_tetro = self.tetro_proxy.dump_next()
        self.fall_time = 0
        self.score = 0

    def handle(self, kevent):
        """ 
        a function to handle keyboard event
        kevent: a PyGame event object
        """
        if kevent.type != pygame.KEYDOWN:
            # illegal event
            return 
        if kevent.key == pygame.K_LEFT:
            # shift left
            self.curr_tetro.left()
            if not self.valid_space():
                self.curr_tetro.right()
        elif kevent.key == pygame.K_RIGHT:
            # shift right
            self.curr_tetro.right()
            if not self.valid_space():
                self.curr_tetro.left()
        elif kevent.key == pygame.K_UP:
            # rotate
            self.curr_tetro.rotate_clockwise()
            if not self.valid_space():
                self.curr_tetro.rotate_counterclockwise()
        elif kevent.key == pygame.K_DOWN:
            # move down
            self.curr_tetro.down()
            if not self.valid_space():
                self.curr_tetro.up()

    def play(self, interface: UserInterface):
        
        self.reset()

        run = True
        while run:

            self.grid = self.update_grid()

            self.clock.tick()

            self.move_downwards()
            
            # User Control Part:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # close the window & quit the program
                    run = False
                    interface.shutdown()
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.handle(event)

            shape_pos = self.tetro_proxy.convert_shape_format(self.curr_tetro)
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    self.grid[y][x] = self.curr_tetro.color

            if self.curr_tetro.check_die():
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    self.occupied_positions[p] = self.curr_tetro.color
                self.curr_tetro = self.tetro_proxy.dump_next()
                # update score when rows are eliminated:
                cleared = self.eliminate_row()
                if cleared > 0:
                    self.score += self.compute_score(cleared)

            interface.draw_window(self.grid)
            interface.draw_next_shape(self.tetro_proxy.view_next())
            interface.update()

            if self.fail():
                run = False

        interface.draw_text_middle("You Lose. Score:{}".format(self.score), 40, (255,255,255))
        interface.update()
        pygame.time.delay(2000)

        return self.score
