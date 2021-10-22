## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Liu
## ----------------------------------------


import pygame
from utils import *


class Gameboard(object):
    def __init__(self, column, row, tetro_proxy):
        self.column = column
        self.row = row
        self.tetro_proxy = tetro_proxy
        self.clock = pygame.time.Clock()

    def update_grid(self, occupied: dict):
        grid = [[(0,0,0) for x in range(self.column)] for x in range(self.row)]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in occupied:
                    c = occupied[(j,i)]
                    grid[i][j] = c
        return grid        

    def valid_space(self, shape, grid):
        accepted_positions = [[(j, i) for j in range(self.column) if grid[i][j] == (0,0,0)] for i in range(self.row)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = self.tetro_proxy.convert_shape_format(shape)
        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False
        return True

    def eliminate_row(self, grid, locked):
        inc = 0
        for i in range(len(grid)-1,-1,-1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)
                    
    def fail(self, occupied):
        for pos in occupied:
            x, y = pos
            if y < 1:
                return True
        return False
        
    def play(self, window):

        change_tetro = False
        fall_time = 0
        fall_speed = 0.27
        score = 0

        occupied_positions = {}
        grid = self.update_grid(occupied=occupied_positions)

        curr_tetro = self.tetro_proxy.dump_next()

        run = True
        while run:

            grid = self.update_grid(occupied=occupied_positions)
            fall_time += self.clock.get_rawtime()
            self.clock.tick()
            
            if fall_time/1000 >= fall_speed:
                fall_time = 0
                curr_tetro.y += 1
                if not (self.valid_space(curr_tetro, grid)) and curr_tetro.y > 0:
                    curr_tetro.y -= 1
                    change_tetro = True
            
            shape_pos = self.tetro_proxy.convert_shape_format(curr_tetro)
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = curr_tetro.color

            if change_tetro:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    occupied_positions[p] = curr_tetro.color
                curr_tetro = self.tetro_proxy.dump_next()
                change_tetro = False
                if self.eliminate_row(grid, occupied_positions):
                    score += 10

            draw_window(grid, window)
            draw_next_shape(self.tetro_proxy.view_next(), window)
            pygame.display.update()

            if self.fail(occupied_positions):
                run = False

        draw_text_middle("You Lose", 40, (255,255,255), window)
        pygame.display.update()
        pygame.time.delay(2000)
