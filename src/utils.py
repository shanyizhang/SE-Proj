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

    surface.blit(label, (top_left_x + board_width/2 - (label.get_width() / 2), top_left_y + board_height/2 - label.get_height()/2))
