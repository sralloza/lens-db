from collections import namedtuple
from smtplib import SMTPConnectError
from unittest import mock

import pytest

from lens_db.email import send_email

Interface = namedtuple("UnencryptedCredentials", ["username", "password"])


@pytest.fixture(params=["example@example.com", None])
def destinations(request):
    return request.param


@pytest.fixture(params=["subject", None])
def subject(request):
    return request.param


@pytest.fixture(params=["message", None])
def message(request):
    return request.param


@mock.patch("lens_db.email.SMTP")
@mock.patch("lens_db.email.get_credentials")
def test_callings_1(get_creds_mock, smtp_mock, destinations, subject, message):
    get_creds_mock.return_value = Interface("--user--", "--pass--")
    raises = not (destinations and subject and message)
    if raises:
        with pytest.raises(TypeError):
            send_email(destinations, subject, message)
    else:
        result = send_email(destinations, subject, message)
        assert result


@mock.patch("lens_db.email.SMTP")
@mock.patch("lens_db.email.get_credentials")
def test_callings_2(get_creds_mock, smtp_mock):
    with pytest.raises(TypeError):
        send_email("destinations", "subject", "message", retries=2 + 2j)


@mock.patch("lens_db.email.SMTP")
@mock.patch("lens_db.email.get_credentials")
def test_normal(get_creds_mock, smtp_mock):
    get_creds_mock.return_value = Interface("--user--", "--pass--")

    result = send_email("destinations", "subject", "message", name="name")
    assert result

    smtp_mock.assert_called_once_with("smtp.gmail.com", 587)
    server = smtp_mock.return_value
    server.starttls.assert_called_once_with()
    server.login.assert_called_once_with("--user--", "--pass--")

    server.sendmail.assert_called_once()
    assert server.sendmail.call_args_list[0][0][:2] == ("--user--", ["destinations"])
    server.quit.assert_called_once_with()


@mock.patch("lens_db.email.logger")
@mock.patch("lens_db.email.SMTP")
@mock.patch("lens_db.email.get_credentials")
def test_errors(get_creds_mock, smtp_mock, logger_mock):
    get_creds_mock.return_value = Interface("--user--", "--pass--")
    server = mock.MagicMock()
    smtp_mock.side_effect = [SMTPConnectError(-1, "custom call")] * 3 + [server]

    result = send_email("destinations", "subject", "message", name="name")
    assert result

    smtp_mock.assert_any_call("smtp.gmail.com", 587)
    assert smtp_mock.call_count == 4

    server.starttls.assert_called_once_with()
    server.login.assert_called_once_with("--user--", "--pass--")

    server.sendmail.assert_called_once()
    assert server.sendmail.call_args_list[0][0][:2] == ("--user--", ["destinations"])
    server.quit.assert_called_once_with()

    logger_mock.debug.assert_called_once()
    assert logger_mock.warning.call_count == 3


@mock.patch("lens_db.email.logger")
@mock.patch("lens_db.email.SMTP")
@mock.patch("lens_db.email.get_credentials")
def test_critical_error(get_creds_mock, smtp_mock, logger_mock):
    get_creds_mock.return_value = Interface("--user--", "--pass--")
    smtp_mock.side_effect = SMTPConnectError(-1, "Custom call")

    result = send_email("destinations", "subject", "message", name="name")
    assert not result

    smtp_mock.assert_any_call("smtp.gmail.com", 587)
    assert smtp_mock.call_count == 5
    server = smtp_mock.return_value

    # Error in in SMTP, rest methods not called
    server.starttls.assert_not_called()
    server.login.assert_not_called()

    server.sendmail.assert_not_called()
    server.quit.assert_not_called()

    logger_mock.debug.assert_called_once()
    assert logger_mock.warning.call_count == 5
    logger_mock.critical.assert_called_once()
