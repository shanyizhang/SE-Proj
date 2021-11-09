## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import sqlite3


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
        print(len(rows) > 0)
        return len(rows) > 0

    def show_all(self):
        rows = self.cursor.execute("SELECT name, score FROM leaderboard").fetchall()
        print(rows)