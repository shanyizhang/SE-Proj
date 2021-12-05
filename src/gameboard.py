## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import pygame
from tetro import Tetromino, TetrominoProxy
from display import *
import numpy as np
from model import CNNModel, DeterministicModel
import torch
import os
import random
from config import *


FALL_SPEED_CANDIDATE = [0.6, 0.3, 0.1]
EXPLORE_EXPLOIT_TRADEOFF_CANDIDATE = [0.3, 0.6, 0.9]

class Gameboard(object):
    def __init__(self, column, row, tetro_proxy, diff):
        """
        Init the Gameboard
        Input: number of columns and rows, tetro proxy and difficulty level 
        Output: None
        """
        self.column = column
        self.row = row
        self.tetro_proxy : TetrominoProxy = tetro_proxy
        self.clock = pygame.time.Clock()
        
        self.fall_speed = FALL_SPEED_CANDIDATE[diff]
        self.explore_exploit_tradeoff = EXPLORE_EXPLOIT_TRADEOFF_CANDIDATE[diff]

        self.grid = None
        self.occupied_positions = None
        self.curr_tetro : Tetromino = None
        self.fall_time = None
        self.score = None
        self.model = None

    def update_grid(self):
        """
        Update the grid given the current situation
        Input: None
        Output: Grid representation
        """
        grid = [[(0,0,0) for x in range(self.column)] for x in range(self.row)]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in self.occupied_positions:
                    c = self.occupied_positions[(j,i)]
                    grid[i][j] = c
        return grid        

    def valid_space(self):
        """
        Check the movement of the tetromino is valid or not
        Input: None
        Output: Boolean indicating if it is valid 
        """
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
        Compute the score when rows are cleared
        Input: number of rows being cleared (between 1 to 4)
        Output: Score
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
        """
        Eliminate rows that are full when the tetromino hits the bottom
        Input: None
        Output: Number of rows eliminated
        """
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
        """ Check if the user fail the game """
        for pos in self.occupied_positions:
            _, y = pos
            if y < 1:
                return True
        return False

    def move_downwards(self):
        """ 
        The tetromino moves downward after each timestamp
        Input: None
        Output: None
        """
        self.fall_time += self.clock.get_rawtime()
        if self.fall_time/1000 >= self.fall_speed:
            self.fall_time = 0
            self.curr_tetro.down()
            if not self.valid_space() and self.curr_tetro.y > 0:
                self.curr_tetro.up()
                self.curr_tetro.die()

    def reset(self, tetro_init=None):
        """ 
        Reset the state of the gameboard after each play
        Input: None
        Output: None
        """
        self.occupied_positions = dict()
        self.grid = self.update_grid()
        self.curr_tetro = self.tetro_proxy.dump_next(index_next=tetro_init)  # modified
        self.fall_time = 0
        self.score = 0
        if ML:
            self.model = CNNModel(num_class=NUM_TETRO)
            if os.path.exists(CKPT):
                self.model.load_state_dict(torch.load(CKPT))
            self.model.train()
        else:
            self.model = DeterministicModel(num_class=NUM_TETRO)

    def handle(self, kevent):
        """
        Handle events
        Input: event object captured by pygame framework
        Output: None
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

    def boolean_grid(self, torch_flag):
        """
        Convert the grid to boolean for learner
        Input: torch_flag indicating if output torch.tensor or numpy.array
        Output: Grid in the format of array of booleans
        """
        bool_grid = list()
        for i in range(len(self.grid)):
            line = self.grid[i]
            bool_line = [(0, 0, 0) != _ for _ in line]
            bool_grid.append(bool_line)
        bool_grid = 1.0 * np.array(bool_grid)
        if torch_flag:
            bool_grid = np.expand_dims(bool_grid, axis=(0,1))
            bool_grid = torch.from_numpy(bool_grid) # (1, 1, 20, 10) 
            bool_grid = bool_grid.to(torch.float32)
        return bool_grid

    def play(self, interface: UserInterface):
        """
        The main workflow of the game
        Input: the interface handle
        Output: the score achieved in this game
        """        
        
        self.reset()

        if ML:
            optimizer = torch.optim.SGD(self.model.parameters(), lr=0.001)
            criterion = torch.nn.MSELoss()

        first = True
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
                # update score when rows are eliminated:
                cleared = self.eliminate_row()
                if cleared > 0:
                    self.score += self.compute_score(cleared)

                if ML: # activate machine learning 
                    if cleared > 0:
                        if not first:
                            gt = torch.full((NUM_TETRO,), 1/(NUM_TETRO-1))
                            gt[tetris_index] = 0
                            optimizer.zero_grad()
                            loss = criterion(out, gt)
                            loss.backward()
                            optimizer.step()
                            # torch.save(self.model.state_dict(), CKPT)
                            print("Training...")
                        first = False
                    self.grid = self.update_grid()
                    out = self.model(self.boolean_grid(torch_flag=True)) # predict index
                    tetris_index = int(torch.argmax(out))
                    if random.random() < self.explore_exploit_tradeoff:
                        self.curr_tetro = self.tetro_proxy.dump_next(index_next=tetris_index) # Exploitation
                    else:
                        self.curr_tetro = self.tetro_proxy.dump_next() # Exploration
                else:
                    if random.random() < self.explore_exploit_tradeoff:
                        tetris_exclude = self.model.predict(self.boolean_grid(torch_flag=False)) # Exploitation
                        self.curr_tetro = self.tetro_proxy.dump_next(blacklist_next=tetris_exclude)
                    else:
                        self.curr_tetro = self.tetro_proxy.dump_next() # Exploration

            interface.draw_window(self.grid)
            interface.draw_next_shape(self.tetro_proxy.view_next())
            interface.update()

            if self.fail():
                run = False

        interface.draw_text_middle("You Lose. Score:{}".format(self.score), 40, (255,255,255))
        interface.update()
        pygame.time.delay(2000)

        return self.score
