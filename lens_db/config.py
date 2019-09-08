from datetime import timedelta
from pathlib import Path

__all__ = ['LENS_DURABILITY', 'LENS_DURABILITY_DELTA', 'ADMIN_EMAIL', 'LOGGING_PATH',
           'DATABASE_PATH']

LENS_DURABILITY = 15  # In days
LENS_DURABILITY_DELTA = timedelta(days=LENS_DURABILITY)
ADMIN_EMAIL = 'sralloza@gmail.com'

LOGGING_PATH = Path(__file__).parent.parent / 'lens-db.log'
DATABASE_PATH = Path(__file__).parent.parent / 'lens.db'
