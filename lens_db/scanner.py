import logging
from datetime import datetime, timedelta

from allo_mail import send_email

from lens_db.config import ADMIN_EMAIL, LENS_DURABILITY_DELTA
from lens_db.core import Lens

logger = logging.getLogger(__name__)


def scan():
    last = Lens.get_last()
    if not last:
        logger.debug('No entries')
        return

    today = today_date()
    delta = today - last
    logger.debug('Calculated delta of %s days', delta.days)

    if delta > LENS_DURABILITY_DELTA:
        logger.debug('Delta > %s days, sending email (expired)', LENS_DURABILITY_DELTA.days)
        message = 'Hay que cambiar las lentillas, el último cambio fue el %s (%s días)' % (
            last, delta)
        return send_email(ADMIN_EMAIL, 'Cambiar lentillas YA', message, name='Lens-db')
    if delta == LENS_DURABILITY_DELTA:
        logger.debug('Delta > %s days, sending email (tomorrow)', LENS_DURABILITY_DELTA.days)
        message = 'Hay que cambiar las lentillas, el último cambio fue el %s (%s días)' % (
            last, delta)
        return send_email(ADMIN_EMAIL, 'Cambiar lentillas mañana', message, name='Lens-db')
    elif delta == LENS_DURABILITY_DELTA - timedelta(days=1):
        logger.debug('Delta > %s days, sending email (day after tomorrow)', LENS_DURABILITY_DELTA.days)
        message = 'Mañana hay que cambiar las lentillas, el último cambio fue el %s (%s días)' % (
            last, delta)
        return send_email(ADMIN_EMAIL, 'Cambiar lentillas pasado mañana', message, name='Lens-db')

    logger.debug('%d days left with current lens', LENS_DURABILITY_DELTA.days - delta.days)


def today_date():
    # TODO: move to other file
    return datetime.today().date()
