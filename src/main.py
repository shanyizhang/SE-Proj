## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Liu
## ----------------------------------------


from gameboard import Gameboard
from config import *
from utils import *
import pygame


if __name__ == '__main__':

    pygame.font.init()

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Tetris Game')

    run = True
    while run:
        window.fill((0,0,0))
        draw_text_middle('Press any key to begin.', 60, (255, 255, 255), window)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                G = Gameboard(column=column, row=row)

    pygame.quit()
