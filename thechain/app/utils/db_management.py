import sqlite3
import pathlib


class DbConnection:
    def __init__(self):
        self.conn = sqlite3.connect(
            pathlib.Path(__file__).parent / 'theblock.db'
            )


