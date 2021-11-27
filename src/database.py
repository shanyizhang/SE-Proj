## ----------------------------------------
##   Software Engineering @ NYU
##   Course Project - Tetris Game
##   Ken S. Zhang & Qingyang Li
## ----------------------------------------


import sqlite3

"""
SQLite Database for Leaderboard
"""

class Leaderboard(object):
    def __init__(self):
        """
        Init the database
        Input: None
        Output: None
        """
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE leaderboard (name TEXT, score INTEGER)")

    def ingest(self, name: str, score: int):
        """
        Ingest a record
        Input: Username and score
        Output: None
        """
        if not self.exist(name):
            self.cursor.execute("INSERT INTO leaderboard VALUES ('{}', {})".format(name, score))
        else:
            self.cursor.execute("UPDATE leaderboard SET score = ? WHERE name = ?",(score, name))

    def exist(self, name):
        """
        Query a record according to name
        Input: Username
        Output: Boolean indicating if it exists
        """
        rows = self.cursor.execute("SELECT name FROM leaderboard WHERE name = ?",(name,),).fetchall()
        return len(rows) > 0

    def show_all(self):
        """
        Display the leaderboard on stdout
        Input: None
        Output: None
        """
        rows = self.cursor.execute("SELECT name, score FROM leaderboard").fetchall()
        print(rows)
    
    def get_sorted(self):
        """
        Return a list of record sorted by score 
        Input: None
        Output: List of record
        """
        query_str = "SELECT name, score FROM leaderboard ORDER BY score DESC"
        rows = self.cursor.execute(query_str).fetchall()
        return rows
