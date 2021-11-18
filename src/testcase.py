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

class TestLeader(unittest.TestCase):
    """ Unit Test for Leader Board """
    def setUp(self) -> None:
        self.lb = Leaderboard()
    
    def test_show_dummy(self):
        """ display some dummy data """
        dummy = [("Karn", 180), ("Bingbing", 170), ("Wei", 169), ("Xia", 172), ("Xiaoran", 175)]
        for row in dummy:
            self.lb.ingest(row[0], row[1])
        self.lb.show_GUI()
        self.assertTrue(True)  # no check available

if __name__ == '__main__':
    unittest.main()
