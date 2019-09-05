import datetime
import logging
import sqlite3
from pathlib import Path

from lens_db.exceptions import AlreadyAddedError

DATABASE_PATH = Path(__file__).parent.parent / 'lens.db'
logger = logging.getLogger(__name__)


class Lens:
    def __init__(self):
        pass

    @staticmethod
    def add(delta_days=0):
        dt = datetime.datetime.today() - datetime.timedelta(days=delta_days)
        dt_string = dt.strftime('%Y-%m-%d')

        logger.debug('Adding to lens-database: %r', dt_string)
        Lens.add_custom(dt_string)

    @staticmethod
    def add_custom(date_string: str):
        datetime.datetime.strptime(date_string, '%Y-%m-%d')

        with DBConnection() as connection:
            try:
                connection.add(date_string)
            except sqlite3.IntegrityError:
                raise AlreadyAddedError('Lens %r are already in the database' % date_string)

    @staticmethod
    def get_last():
        with DBConnection() as connection:
            last = connection.get_last()

            logger.debug('Last from database: %r', last)

            if not last:
                return None
            return datetime.datetime.strptime(last, '%Y-%m-%d').date()


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
        try:
            return self.cursor.fetchall()[-1][0]
        except TypeError:  # There are no entries
            return None
