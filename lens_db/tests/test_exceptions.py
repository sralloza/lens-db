import pytest

from lens_db.src.exceptions import BaseLensDBError, AlreadyAddedError, InvalidDateError


def test_base_lens_db_error():
    with pytest.raises(BaseLensDBError):
        raise BaseLensDBError

    assert issubclass(BaseLensDBError, Exception)


def test_already_added_error():
    with pytest.raises(AlreadyAddedError):
        raise AlreadyAddedError

    assert issubclass(AlreadyAddedError, BaseLensDBError)


def test_invalid_date_error():
    with pytest.raises(InvalidDateError):
        raise InvalidDateError

    assert issubclass(InvalidDateError, BaseLensDBError)
