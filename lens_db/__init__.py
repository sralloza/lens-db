from logging import DEBUG, basicConfig
from pathlib import Path

from .src.config import LOGGING_PATH

__all__ = []

basicConfig(
    filename=LOGGING_PATH,
    level=DEBUG,
    format="[%(asctime)s] %(levelname)s - %(module)s:%(lineno)s - %(message)s",
)


def get_version():
    return Path(__file__).with_name("VERSION").read_text().strip()

__version__ = get_version()
