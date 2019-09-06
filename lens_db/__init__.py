import logging
from .config import LOGGING_PATH
logging.basicConfig(
    filename=LOGGING_PATH,
    level=logging.DEBUG,
    format='%(asctime)s] %(levelname)s - %(module)s:%(lineno)s - %(message)s')
