from datetime import datetime
from typing import Type


def today_date():
    """Returns today's date."""
    return datetime.today().date()


def exception_exit(exception: Type[Exception]):
    """Exists the progam showing an exception.

    Args:
        Exception: Exception to show.

    """
    exit('%s: %s' % (exception.__class__.__name__, ', '.join(exception.args)))
