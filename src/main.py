## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


from database import Leaderboard
from gameboard import Gameboard
from tetro import *
from config import *
from display import *
import pygame


def main(interface: UserInterface):
    TP = TetrominoProxy(column=COLUMN)
    GB = Gameboard(column=COLUMN, row=ROW, tetro_proxy=TP)
    score = GB.play(interface)
    return score


if __name__ == '__main__':

    LB = Leaderboard()

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
        UI.update()

        if IB.check_complete():
            
            name = IB.dump_and_flush()
            IB.update_display_text()  # dump InputBox display
            score = main(interface=UI)

            LB.ingest(name, score)
            LB.show_all()

    pygame.quit()
