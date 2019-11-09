from datetime import timedelta
from pathlib import Path


def test_lens_durability():
    from lens_db.config import LENS_DURABILITY

    assert isinstance(LENS_DURABILITY, int)


def test_lens_durability_delta():
    from lens_db.config import LENS_DURABILITY_DELTA

    assert isinstance(LENS_DURABILITY_DELTA, timedelta)


def test_admin_email():
    from lens_db.config import ADMIN_EMAIL

    assert isinstance(ADMIN_EMAIL, str)


def test_logging_path():
    from lens_db.config import LOGGING_PATH

    assert isinstance(LOGGING_PATH, Path)
    assert LOGGING_PATH.suffix == ".log"
    assert LOGGING_PATH.name == "lens-db.log"


def test_database_path():
    from lens_db.config import DATABASE_PATH

    assert isinstance(DATABASE_PATH, Path)
    assert DATABASE_PATH.suffix == ".db"
    assert DATABASE_PATH.name == "lens.db"
