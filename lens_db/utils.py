from datetime import datetime


def today_date():
    return datetime.today().date()


def exception_exit(exception):
    exit('%s: %s' % (exception.__class__.__name__, ', '.join(exception.args)))
