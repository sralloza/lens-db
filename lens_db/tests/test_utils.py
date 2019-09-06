from datetime import datetime

from lens_db.utils import today_date


def test_today_date():
    assert today_date() == datetime.today().date()