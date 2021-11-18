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


def main(interface: UserInterface, diff):

    TP = TetrominoProxy(column=COLUMN)
    GB = Gameboard(column=COLUMN, row=ROW, tetro_proxy=TP, diff=diff)
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
            UI.checkbox.handle_event(event)

        UI.checkbox.update_checkbox_array()
        UI.inputbox.update_inputbox()
        UI.update()

        time.sleep(0.15)

        if UI.inputbox.check_complete() and UI.checkbox.check_complete():
            
            name = UI.inputbox.dump_and_flush()
            diff = UI.checkbox.dump_and_flush()
            #UI.inputbox.update_display_text()  # dump InputBox display
            score = main(interface=UI, diff=diff)

            LB.ingest(name, score)
            LB.show_all()

    pygame.quit()
