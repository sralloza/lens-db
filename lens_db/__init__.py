from logging import basicConfig, DEBUG

from .config import LOGGING_PATH

basicConfig(
    filename=LOGGING_PATH,
    level=DEBUG,
    format='%(asctime)s] %(levelname)s - %(module)s:%(lineno)s - %(message)s')
