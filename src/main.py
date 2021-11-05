## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


from gameboard import Gameboard
from tetro import *
from config import *
from display import *
import pygame


def main(interface: UserInterface):
    TP = TetrominoProxy(column=COLUMN)
    GB = Gameboard(column=COLUMN, row=ROW, tetro_proxy=TP)
    GB.play(interface)


if __name__ == '__main__':

    UI = UserInterface()

    run = True
    while run:

        UI.start()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(interface=UI)

    pygame.quit()
