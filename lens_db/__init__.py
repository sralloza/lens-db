from logging import DEBUG, basicConfig

from ._version import get_versions
from .src.config import LOGGING_PATH

__version__ = get_versions()["version"]
del get_versions

__all__ = []

basicConfig(
    filename=LOGGING_PATH,
    level=DEBUG,
    format="[%(asctime)s] %(levelname)s - %(module)s:%(lineno)s - %(message)s",
)
