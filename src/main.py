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
import time


def main(interface: UserInterface):
    TP = TetrominoProxy(column=COLUMN)
    GB = Gameboard(column=COLUMN, row=ROW, tetro_proxy=TP)
    score = GB.play(interface)
    return score


if __name__ == '__main__':

    LB = Leaderboard()

    UI = UserInterface()

    run = True

    while run:

        UI.start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            UI.inputbox.handle_event(event)

        UI.inputbox.update_display_text()
        UI.inputbox.draw_rect()
        UI.update()

        time.sleep(0.15)

        if UI.inputbox.check_complete():
            
            name = UI.inputbox.dump_and_flush()
            UI.inputbox.update_display_text()  # dump InputBox display
            score = main(interface=UI)

            LB.ingest(name, score)
            LB.show_all()

    pygame.quit()
