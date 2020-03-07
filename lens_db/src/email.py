import logging
import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .credentials import get_credentials

logger = logging.getLogger(__name__)

__all__ = ["send_email"]


def send_email(destinations, subject, message, name=None, retries=5):
    """Sends an email.

    Args:
        destinations (list or str): destination or list of destinations of the email.
        subject (str): subject of the email
        message (str): message of the email..
        name (str): name of the sender (only needed in same cases).
        retries (int): retries in case of error.

    Returns:
        bool: True if everything went ok, False otherwise.

    """

    if destinations is None or subject is None or message is None:
        raise TypeError(f"destinations, subject and message can not be None")

    if not isinstance(retries, int):
        raise TypeError(f"retries must be int, not {type(retries).__name__}")

    email_credentials = get_credentials()

    logger.debug(
        "Sending email from %r to %r (%s)",
        email_credentials.username,
        destinations,
        subject,
    )

    if isinstance(destinations, str):
        destinations = [
            destinations,
        ]

    msg = MIMEMultipart()

    if name:
        msg["From"] = f"{name} <{email_credentials.username}>"
    else:
        msg["From"] = email_credentials.username

    msg["To"] = ", ".join(destinations)
    msg["Subject"] = subject

    body = message.replace("\n", "<br>")
    msg.attach(MIMEText(body, "html"))

    while retries > 0:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
        except (smtplib.SMTPConnectError, socket.gaierror):
            retries -= 1
            logger.warning("SMTP Connection Error")
            continue

        server.starttls()
        server.login(email_credentials.username, email_credentials.password)

        server.sendmail(email_credentials.username, destinations, msg.as_string())
        server.quit()
        return True

    logger.critical("Retries exceeded")
    return False
