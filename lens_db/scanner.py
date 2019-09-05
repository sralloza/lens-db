import logging
from datetime import datetime

from allo_mail import send_email

from lens_db.config import ADMIN_EMAIL, LENS_DURABILITY_DELTA
from lens_db.core import Lens

logger = logging.getLogger(__name__)


def scan():
    last = Lens.get_last()
    if not last:
        logger.debug('No entries')
        return

    today = datetime.today().date()
    delta = today - last
    logger.debug('Calculated delta of %s days', delta.days)

    if delta > LENS_DURABILITY_DELTA:
        logger.debug('Delta > %s days, sending email', LENS_DURABILITY_DELTA.days)
        message = 'Hay que cambiar las lentillas, el último cambio fue el %s (%s días)' % (
            last, delta)
        return send_email(ADMIN_EMAIL, 'Cambiar lentillas', message, name='Lens-db')

    logger.debug('%d days left with current lens', LENS_DURABILITY_DELTA.days - delta.days)
