from datetime import datetime


def today_date():
    """Returns today's date."""
    return datetime.today().date()


def exception_exit(exception):
    """Exists the progam showing an exception.

    Args:
        exception: Exception to show.

    Raises:
        TypeError: if exception is not a subclass of Exception.

    """

    if not issubclass(exception, Exception):
        raise TypeError('exception should be a subclass of Exception')

    exit('%s: %s' % (exception.__class__.__name__, ', '.join(exception.args)))
