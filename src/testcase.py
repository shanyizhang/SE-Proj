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
from model import Model
from tetro import *
import torch


class TestDisplay(unittest.TestCase):
    """ Unit Test for class UserInterface & Leaderboard """

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
        """ display User Interface """
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


class TestModel(unittest.TestCase):
    """ Unit Test for class Model """

    def setUp(self):
        self.model = None  # a CNN Model

    def tearDown(self):
        pass

    def test_cnn_model(self):
        """ test CNN model """
        self.model = Model(num_class=NUM_TETRO)
        input = torch.rand(size=(1, 1, 20, 10))
        with torch.no_grad():
            out = self.model(input) 
            self.assertTrue(out.shape == torch.Size([NUM_TETRO]))


class TestTetromino(unittest.TestCase):
    """ Unit Test for class Tetromino & TetrominoProxy """

    def setUp(self):
        self.tetroProxy = None  # a TetrominoProxy

    def tearDown(self):
        pass

    def test_tetromino_proxy(self):
        """ test TetrominoProxy & Tetromino """
        self.tetroProxy = TetrominoProxy(column=COLUMN)
        _ = self.tetroProxy.dump_next(index_next=1)
        tetro = self.tetroProxy.view_next()
        self.assertTrue(tetro.x == COLUMN/2)
        self.assertTrue(tetro.y == 0)
        self.assertTrue(tetro.shape == SHAPES[1])
        self.assertTrue(tetro.color == COLORS[1])
        self.assertTrue(tetro.rotation == 0)
        self.assertTrue(tetro.state == TetroState.Alive)
        tetro.down()
        tetro.up()
        tetro.left()
        tetro.right()
        tetro.rotate_clockwise()
        tetro.rotate_clockwise()
        self.assertTrue(tetro.x == COLUMN/2)
        self.assertTrue(tetro.y == 0)      
        self.assertTrue(tetro.rotation == 0) 
        

if __name__ == '__main__':
    unittest.main()
