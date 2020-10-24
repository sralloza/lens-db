import logging
import sqlite3
from datetime import datetime, timedelta, date
from typing import Union, Optional, List

from .config import DATABASE_PATH
from .exceptions import AlreadyAddedError, InvalidDateError
from .utils import today_date

logger = logging.getLogger(__name__)

date_or_none = Union[date, None]
list_of_str = List[str]

__all__ = ["Lens", "DBConnection"]


class Lens:
    """Class to manage when are lens packages opened."""

    def __new__(cls, *args, **kwargs):
        raise NotImplementedError("Lens shouldn't be instanciated.")

    @staticmethod
    def add(delta_days=0):
        """Adds a timestamp of delta_days days ago.

        Args:
            delta_days (int): number of days since package was opened.

        Raises:
            AlreadyAddedError: if the timestamp is already in the database.

        """
        dt = today_date() - timedelta(days=delta_days)
        dt_string = dt.strftime("%Y-%m-%d")

        logger.debug("Adding to lens-database: %r", dt_string)
        Lens.add_custom(dt_string)

    @staticmethod
    def add_custom(date_string: str):
        """Adds a timestamp to the database from a string.

        Args:
            date_string (str): string of the datetime in format YYYY-MM-DD

        Raises:
            InvalidDateError: if the format of date_string is incorrect.
            AlreadyAddedError: if the timestamp is already in the database.

        """
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            raise InvalidDateError(
                "%r is not a valid date format (use 2019-12-31)" % date_string
            )

        with DBConnection() as connection:
            try:
                connection.add(date_string)
            except sqlite3.IntegrityError:
                raise AlreadyAddedError(
                    "Lens %r are already in the database" % date_string
                )

    @staticmethod
    def get_last() -> date_or_none:
        """Returns the last date inserted in the database or None, if the database is empty."""

        with DBConnection() as connection:
            last = connection.get_last()

            logger.debug("Last from database: %r", last)

            if not last:
                return None
            return datetime.strptime(last, "%Y-%m-%d").date()

    @staticmethod
    def list() -> list_of_str:
        """Returns a list of every timestamp registered in the database."""
        with DBConnection() as connection:
            return connection.list()


class DBConnection:
    """Represents a sqlite database connection."""

    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_PATH.as_posix())
        self.cursor = self.connection.cursor()

        self.ensure_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()

    def commit(self):
        """Commits changes."""
        self.connection.commit()

    def close(self):
        """Closes the database."""
        self.cursor.close()
        self.connection.close()

    def ensure_table(self):
        """Creates the table 'lens' if it does not exist."""
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS 'lens' (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL UNIQUE
                        )"""
        )

    def add(self, time_str):
        """Adds the time_str to the database.

        Args:
            time_str (str): time string to add to the database.
        """
        self.cursor.execute("INSERT INTO lens VALUES (NULL, ?)", [time_str])

    def get_last(self) -> Optional[str]:
        """Returns the last time string of the database."""
        try:
            return self.list()[-1]
        except IndexError:  # There are no entries
            return None

    def list(self) -> list_of_str:
        """Returns a list with every time string in the database."""
        self.cursor.execute("SELECT timestamp FROM lens ORDER BY timestamp")
        return sorted([x[0] for x in self.cursor.fetchall()])
