## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import unittest
import time
from gameboard import Gameboard
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


class TestGameBoard(unittest.TestCase):
    """ Unit Test for class Gameboard """

    def setUp(self) -> None:
        self.tp = TetrominoProxy(COLUMN)
        self.gb = Gameboard(COLUMN, ROW, self.tp, 2)
        self.ui = UserInterface(show_window=True)

    def tearDown(self) -> None:
        self.tp = None
        self.gb = None

    def test_play_noop(self):
        """ test the play() method without user operations """
        print("# Start playing ...")
        _score = self.gb.play(self.ui)  # run the play() method
        self.assertEqual(_score, 0)  # no score gained

    def test_reset(self):
        """ test the reset() method """
        self.gb.reset()
        self.assertEqual(self.gb.score, 0)  # initial score is 0
        self.assertEqual(self.gb.fall_time, 0)  # fall time is 0
        self.assertEqual(self.gb.occupied_positions, {})  # no grid is occupied
        self.assertIsInstance(self.gb.curr_tetro, Tetromino)  # initial Tetromino randomly picked

    def test_update_grid(self):
        """ test the update_grid() method """
        self.gb.reset()  # reset Gameboard
        # choose a grid to occupy
        position = (2, 4)
        color = (255, 0, 0)
        self.gb.occupied_positions = {position:color}
        grids = self.gb.update_grid()
        self.assertEqual(grids[position[1]][position[0]], color)
        # front-end display
        self.ui.draw_window(grids)
        self.ui.update()
        time.sleep(3)

    def test_eliminate_row(self):
        """ test the eliminate_row() method """
        self.gb.reset()
        line = 16
        for i in range(self.gb.column):
            self.gb.occupied_positions[(i, line)] = (0, 255, 0)
        self.gb.occupied_positions[(2, 4)] = (255, 0, 0)
        # before elimination
        self.gb.grid = self.gb.update_grid()
        self.ui.draw_window(self.gb.grid)
        self.ui.update()
        time.sleep(4)
        # after elimination
        num = self.gb.eliminate_row()  # call the method
        self.assertEqual(num, 1)
        self.gb.grid = self.gb.update_grid()
        self.ui.draw_window(self.gb.grid)
        self.ui.update()
        time.sleep(4)

    def test_not_fail(self):
        """ fail() method, should return False """
        self.gb.reset()
        positions = [(2, 1), (1, 1), (2, 7)]
        color = (0, 0, 255)
        for pos in positions:
            self.gb.occupied_positions[pos] = color
        grids = self.gb.update_grid()
        self.assertFalse(self.gb.fail())
        #self.ui.draw_window(grids)
        #self.ui.update()
        #time.sleep(4)

    def test_fail(self):
        """ fail() method, should return True """
        self.gb.reset()
        positions = [(2, 1), (1, 1), (2, 7), (2, 0), (9, 0)]
        color = (0, 0, 255)
        for pos in positions:
            self.gb.occupied_positions[pos] = color
        grids = self.gb.update_grid()
        self.assertTrue(self.gb.fail())
        #self.ui.draw_window(grids)
        #self.ui.update()
        #time.sleep(4)

    def test_move_downwards(self):
        """
        test the move_downwards() method
        (the happy path)
        """
        self.gb.reset(tetro_init=0)
        self.gb.clock.tick()
        time.sleep(2)  # wait for some time
        self.gb.clock.tick()
        self.gb.move_downwards()  # should move one grid down
        grids = self.gb.update_grid()
        # check if the current Tetromino is alive
        self.assertFalse(self.gb.curr_tetro.check_die())
        # check its position
        self.assertEqual(self.gb.curr_tetro.y, 1)
        #self.ui.draw_window(grids)
        #self.ui.update()
        #time.sleep(4)

    def test_boolean_grid(self):
        """ test the boolean_grid() method """
        self.gb.reset()
        positions = [(2, 1), (1, 1), (2, 7)]
        color = (0, 0, 255)
        for pos in positions:
            self.gb.occupied_positions[pos] = color
        self.gb.grid = self.gb.update_grid()
        b_grids = self.gb.boolean_grid()
        positions_2 = [(5, 3), (1, 4), (2, 8)]
        for pos in positions:
            # occupied positions
            val = b_grids[0][0][pos[1]][pos[0]]
            self.assertAlmostEqual(float(val), 1.0)
        for pos in positions_2:
            # vacant positions
            val = b_grids[0][0][pos[1]][pos[0]]
            self.assertAlmostEqual(float(val), 0.0)


if __name__ == '__main__':
    unittest.main()
