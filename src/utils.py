## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Liu
## ----------------------------------------


from config import *
import pygame


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + BOARD_WIDTH/2 - (label.get_width() / 2), TOP_LEFT_Y + BOARD_HEIGHT/2 - label.get_height()/2))


def draw_grid(surface):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y
    for i in range(ROW):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i * BLOCK_SIZE), (sx + BOARD_WIDTH, sy + i * BLOCK_SIZE))  
        for j in range(COLUMN):
            pygame.draw.line(surface, (128,128,128), (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + BOARD_HEIGHT))  


def draw_window(grid, surface):
    surface.fill((0,0,0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))
    surface.blit(label, (TOP_LEFT_X + BOARD_WIDTH / 2 - (label.get_width() / 2), BLOCK_SIZE))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    draw_grid(surface)
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, BOARD_WIDTH, BOARD_HEIGHT), 5)


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', BLOCK_SIZE)
    label = font.render('Next Shape', 1, (255,255,255))
    sx = TOP_LEFT_X + BOARD_WIDTH + 50
    sy = TOP_LEFT_Y + BOARD_HEIGHT/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    surface.blit(label, (sx + 10, sy - BLOCK_SIZE))