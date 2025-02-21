import logging
from datetime import timedelta

from colorama import Fore

from .config import ADMIN_EMAIL, DISABLED, DISABLED_PATH, LENS_DURABILITY_DELTA
from .core import Lens
from .email import send_email
from .exceptions import AlreadyDisabledError, AlreadyEnabledError
from .utils import today_date

logger = logging.getLogger(__name__)

__all__ = ["scan"]


def scan():
    """Scanner of the program. If it is needed, an email will be sent."""

    if DISABLED:
        logger.info("DISABLED flag is active, cancelling scan")
        return

    last = Lens.get_last()
    if not last:
        logger.debug("No entries")
        return

    today = today_date()
    delta = today - last
    logger.debug("Calculated delta of %s days", delta.days)

    email_name = "Lens-db"

    if delta == LENS_DURABILITY_DELTA + timedelta(days=1):
        logger.debug(
            "Delta == %s days, sending email (today)", LENS_DURABILITY_DELTA.days + 1
        )
        message = (
            "Hay que cambiar hoy las lentillas, el último cambio fue el %s (%s días)"
            % (last, delta.days)
        )
        return send_email(
            ADMIN_EMAIL, "Cambiar lentillas hoy", message, name=email_name
        )
    if delta > LENS_DURABILITY_DELTA:
        logger.debug(
            "Delta > %s days, sending email (expired)", LENS_DURABILITY_DELTA.days
        )
        message = (
            "Hay que cambiar ya las lentillas, el último cambio fue el %s (%s días)"
            % (last, delta.days)
        )
        return send_email(ADMIN_EMAIL, "Cambiar lentillas YA", message, name=email_name)
    if delta == LENS_DURABILITY_DELTA:
        logger.debug(
            "Delta == %s days, sending email (tomorrow)", LENS_DURABILITY_DELTA.days
        )
        message = (
            "Mañana hay que cambiar las lentillas, el último cambio fue el %s (%s días)"
            % (last, delta.days)
        )
        return send_email(
            ADMIN_EMAIL, "Cambiar lentillas mañana", message, name=email_name
        )
    elif delta == LENS_DURABILITY_DELTA - timedelta(days=1):
        logger.debug(
            "Delta == %s days, sending email (day after tomorrow)",
            LENS_DURABILITY_DELTA.days - 1,
        )
        message = (
            "Pasado mañana hay que cambiar las lentillas, el último cambio fue el %s (%s días)"
            % (last, delta.days)
        )
        return send_email(
            ADMIN_EMAIL, "Cambiar lentillas pasado mañana", message, name=email_name
        )

    logger.debug(
        "%d days left with current lens", LENS_DURABILITY_DELTA.days - delta.days
    )


def disable():
    if DISABLED_PATH.exists():
        raise AlreadyDisabledError("Scan is already disabled")

    DISABLED_PATH.touch()


def enable():
    if not DISABLED_PATH.exists():
        raise AlreadyEnabledError("Scan is already enabled")

    DISABLED_PATH.unlink()


def show_status():
    if DISABLED_PATH.exists():
        print(Fore.LIGHTYELLOW_EX + "Scanner is disabled" + Fore.RESET)
    else:
        print(Fore.LIGHTGREEN_EX + "Scanner is enabled" + Fore.RESET)
