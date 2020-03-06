class BaseLensDBError(Exception):
    """Base lens database exception"""


class AlreadyAddedError(BaseLensDBError):
    """Lens already added error."""


class InvalidDateError(BaseLensDBError):
    """Invalid date error."""


class NoCredentialsError(BaseLensDBError):
    """No credentials error."""
