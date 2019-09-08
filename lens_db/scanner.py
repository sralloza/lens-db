import logging
from datetime import timedelta

from allo_mail import send_email

from .config import ADMIN_EMAIL, LENS_DURABILITY_DELTA
from .core import Lens
from .utils import today_date

logger = logging.getLogger(__name__)

__all__ = ['scan']


def scan():
    """Scanner of the program. If it is needed, an email will be sent."""
    last = Lens.get_last()
    if not last:
        logger.debug('No entries')
        return

    today = today_date()
    delta = today - last
    logger.debug('Calculated delta of %s days', delta.days)

    if delta == LENS_DURABILITY_DELTA + timedelta(days=1):
        logger.debug('Delta == %s days, sending email (today)', LENS_DURABILITY_DELTA.days + 1)
        message = 'Hay que cambiar hoy las lentillas, el último cambio fue el %s (%s días)' % (
            last, delta.days)
        return send_email(ADMIN_EMAIL, 'Cambiar lentillas hoy', message, name='Lens-db')
    if delta > LENS_DURABILITY_DELTA:
        logger.debug('Delta > %s days, sending email (expired)', LENS_DURABILITY_DELTA.days)
        message = 'Hay que cambiar las lentillas, el último cambio fue el %s (%s días)' % (
            last, delta.days)
        return send_email(ADMIN_EMAIL, 'Cambiar lentillas YA', message, name='Lens-db')
    if delta == LENS_DURABILITY_DELTA:
        logger.debug('Delta == %s days, sending email (tomorrow)', LENS_DURABILITY_DELTA.days)
        message = 'Hay que cambiar las lentillas, el último cambio fue el %s (%s días)' % (
            last, delta.days)
        return send_email(ADMIN_EMAIL, 'Cambiar lentillas mañana', message, name='Lens-db')
    elif delta == LENS_DURABILITY_DELTA - timedelta(days=1):
        logger.debug('Delta == %s days, sending email (day after tomorrow)',
                     LENS_DURABILITY_DELTA.days - 1)
        message = 'Mañana hay que cambiar las lentillas, el último cambio fue el %s (%s días)' % (
            last, delta.days)
        return send_email(ADMIN_EMAIL, 'Cambiar lentillas pasado mañana', message, name='Lens-db')

    logger.debug('%d days left with current lens', LENS_DURABILITY_DELTA.days - delta.days)
