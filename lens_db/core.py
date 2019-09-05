import datetime
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent / 'lens.db'


class Lens:
    def __init__(self):
        pass
    @staticmethod
    def add(delta_days=0):
        dt = datetime.datetime.today() - datetime.timedelta(days=delta_days)

        with DBConnection() as connection:
            connection.add(dt.strftime('%Y-%m-%d'))

    def get_last(self):
        with DBConnection() as connection:
            print(connection.get_last())


class DBConnection:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.connection.cursor()

        self.ensure_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def ensure_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS 'lens' (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL UNIQUE                        
                        )""")

    def add(self, time_str):
        self.cursor.execute("INSERT INTO lens VALUES (NULL, ?)", [time_str])

    def get_last(self):
        self.cursor.execute("SELECT timestamp FROM lens")
        return self.cursor.fetchone()[0]


Lens.add()
