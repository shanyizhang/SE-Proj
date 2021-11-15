## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import sqlite3
import tkinter
from tkinter import ttk


class Leaderboard(object):
    def __init__(self):
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE leaderboard (name TEXT, score INTEGER)")

    def ingest(self, name: str, score: int):
        if not self.exist(name):
            self.cursor.execute("INSERT INTO leaderboard VALUES ('{}', {})".format(name, score))
        else:
            self.cursor.execute("UPDATE leaderboard SET score = ? WHERE name = ?",(score, name))

    def exist(self, name):
        rows = self.cursor.execute("SELECT name FROM leaderboard WHERE name = ?",(name,),).fetchall()
        return len(rows) > 0

    def show_all(self):
        rows = self.cursor.execute("SELECT name, score FROM leaderboard").fetchall()
        print(rows)
    
    def show_GUI(self, table=None):
        """
        a GUI of LeaderBoard, powered by Tkinter
        the 'table' parameter is used for inputing dummy data
        """
        if table is None:
            # query the sorted data from Database
            query = "SELECT name, score FROM leaderboard ORDER BY score DESC"
            table = self.cursor.execute(query).fetchall()
        board = tkinter.Tk()
        board.title("Leader Board")
        tree = ttk.Treeview(board)  # a table
        tree["columns"] = ("Player", "Score")  # setup the columns
        tree.column("Player", width=100)
        tree.column("Score", width=100)
        tree.heading("Player", text="Player")
        tree.heading("Score", text="Score")
        num = len(table)
        for i in range(num):
            # insert a row of data:
            tree.insert("", i, values=table[i], text="No. %d" % (i + 1))
        tree.pack()
        board.mainloop()
