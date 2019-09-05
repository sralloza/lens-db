class BaseLensDBError(Exception):
    """Base lens database exception"""


class AlreadyAddedError(BaseLensDBError):
    """Lens already added error."""
