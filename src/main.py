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

    IB = InputBox(window=UI.window)
    
    while run:

        UI.start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            IB.handle_event(event)

        IB.update_display_text()
        IB.draw_rect()

        if IB.check_complete():
            text = IB.dump_and_flush()
            print(text)
            main(interface=UI)

    pygame.quit()
