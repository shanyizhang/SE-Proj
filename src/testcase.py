## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import unittest
import time
import pygame
from config import *
from display import *
from database import *

class TestDisplay(unittest.TestCase):
    """ Unit Test for class UserInterface """
    def setUp(self):
        self.ui = None  # a User Interface

    def tearDown(self):
        self.ui.shutdown()

    def test_hide_interface(self):
        """ hide user interface """
        self.ui = UserInterface(show_window=False)
        self.ui.start()
        time.sleep(2)
        self.assertFalse(pygame.display.get_active())

    def test_show_interface(self):
        """ display user interface """
        self.ui = UserInterface(show_window=True)
        self.ui.start()
        time.sleep(2)
        self.assertTrue(pygame.display.get_active())
    
    def test_show_leader(self):
        """ display Leader Board, dummy data used """
        dummy = [
            ("Washington", 100), ("Clinton", 85), ("Obama", 75), ("Trump", 0)
        ]
        self.ui = UserInterface(show_window=True)
        self.ui.start()
        self.ui.draw_leader_board(dummy)
        self.assertTrue(True)
    
    def test_show_leader_2(self):
        """ display Leader Board, query from database """
        dummy = [
            ("Bush", 60), ("Obama", 75), ("Trump", 0), ("Biden", 30)
        ]
        dummy_lb = Leaderboard()
        for row in dummy:
            dummy_lb.ingest(row[0], row[1])
        self.ui = UserInterface(show_window=True)
        self.ui.start()
        self.ui.draw_leader_board(dummy_lb.get_sorted())
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
