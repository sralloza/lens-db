from datetime import datetime

import pytest

from lens_db.utils import today_date, exception_exit


def test_today_date():
    assert today_date() == datetime.today().date()


exceptions = (
    (ValueError, 'Invalid path'),
    (TypeError, ('Invalid type', 'Expected int')),
    (ImportError, 'Module not found: math')
)


@pytest.mark.parametrize('exception, args', exceptions)
def test_exception_exit(exception, args):
    if not isinstance(args, str):
        message = ', '.join(args)
    else:
        message = args
        args = (args, )

    with pytest.raises(SystemExit, match=message):
        try:
            raise exception(*args)
        except Exception as err:
            exception_exit(err)
