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

    """ Main function: Put all ingredients all together """
    TP = TetrominoProxy(column=COLUMN)
    GB = Gameboard(column=COLUMN, row=ROW, tetro_proxy=TP, diff=diff)
    score = GB.play(interface)

    return score


if __name__ == '__main__':

    LB = Leaderboard()

    UI = UserInterface()

    run = True

    while run:

        """ Run the game until the user quit manually """
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
            
            """ Main Game """
            score = main(interface=UI, diff=diff)

            LB.ingest(name, score)
            LB.show_all()
            data = LB.get_sorted()  # query from database
            UI.draw_leader_board(data)  # front-end display of LB

    pygame.quit()
