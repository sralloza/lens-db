from datetime import datetime

__all__ = ["today_date", "exception_exit"]


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


    try:
        raise exception
    except TypeError as exc:
        if exc.args == ("exceptions must derive from BaseException", ):
            raise TypeError("exception should be a subclass of Exception") from exc
    except Exception:
        pass

    exit("%s: %s" % (exception.__class__.__name__, ", ".join(exception.args)))
