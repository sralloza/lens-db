from datetime import date, timedelta
from enum import Enum
from unittest import mock

import pytest
from colorama import Fore

from lens_db.exceptions import AlreadyDisabledError, AlreadyEnabledError
from lens_db.scanner import disable, enable, scan, show_status


class ScanCode(Enum):
    no_entries = 1
    not_sent = 2
    day_after_tomorrow = 3
    tomorrow = 4
    today = 5
    expired = 6


class TestScan:
    @pytest.fixture
    def mocks(self):
        get_last = mock.patch("lens_db.scanner.Lens.get_last").start()
        today_date = mock.patch("lens_db.scanner.today_date").start()
        send_email = mock.patch("lens_db.scanner.send_email").start()

        yield get_last, today_date, send_email

        mock.patch.stopall()

    scan_data = (
        (None, ScanCode.no_entries),
        (5, ScanCode.not_sent),
        (10, ScanCode.not_sent),
        (13, ScanCode.not_sent),
        (14, ScanCode.day_after_tomorrow),
        (15, ScanCode.tomorrow),
        (16, ScanCode.today),
        (17, ScanCode.expired),
        (20, ScanCode.expired),
        (21, ScanCode.expired),
    )

    @pytest.mark.parametrize("days, expect", scan_data)
    def test_scan(self, mocks, days, expect, caplog):
        get_last, today_date, send_email = mocks
        if expect != ScanCode.no_entries:
            get_last.return_value = date(2019, 1, 1)
            today_date.return_value = get_last.return_value + timedelta(days=days)
        else:
            get_last.return_value = None
            today_date.return_value = date(2019, 1, 1)

        scan()

        if expect == ScanCode.no_entries:
            assert "No entries\n" in caplog.text
        elif expect == ScanCode.not_sent:
            send_email.assert_not_called()
        elif expect == ScanCode.day_after_tomorrow:
            send_email.assert_called_once()
            assert "sending email (day after tomorrow)\n" in caplog.text
        elif expect == ScanCode.tomorrow:
            send_email.assert_called_once()
            assert "sending email (tomorrow)\n" in caplog.text
        elif expect == ScanCode.today:
            send_email.assert_called_once()
            assert "sending email (today)\n" in caplog.text
        elif expect == ScanCode.expired:
            send_email.assert_called_once()
            assert "sending email (expired)\n" in caplog.text

    @mock.patch("lens_db.scanner.DISABLED", True)
    def test_disabled(self, mocks, caplog):
        get_last, today_date, send_email = mocks

        scan()

        get_last.assert_not_called()
        today_date.assert_not_called()
        send_email.assert_not_called()


@pytest.mark.parametrize("disabled", [True, False])
@mock.patch("lens_db.scanner.DISABLED_PATH")
def test_disable(dis_path_mock, disabled):
    dis_path_mock.exists.return_value = disabled

    if disabled:
        with pytest.raises(AlreadyDisabledError):
            disable()
        dis_path_mock.touch.assert_not_called()
    else:
        disable()
        dis_path_mock.touch.assert_called_once()

    dis_path_mock.exists.assert_called_once()


@pytest.mark.parametrize("disabled", [True, False])
@mock.patch("lens_db.scanner.DISABLED_PATH")
def test_enable(dis_path_mock, disabled):
    dis_path_mock.exists.return_value = disabled

    if not disabled:
        with pytest.raises(AlreadyEnabledError):
            enable()
        dis_path_mock.unlink.assert_not_called()
    else:
        enable()
        dis_path_mock.unlink.assert_called_once()

    dis_path_mock.exists.assert_called_once()


@pytest.mark.parametrize("disabled", [False, True])
@mock.patch("lens_db.scanner.DISABLED_PATH")
def test_show_status(dis_path_mock, disabled, capsys):
    dis_path_mock.exists.return_value = disabled
    show_status()

    captured = capsys.readouterr()
    if disabled:
        assert "disabled" in captured.out
        assert Fore.LIGHTYELLOW_EX in captured.out
    else:
        assert "enabled" in captured.out
        assert Fore.LIGHTGREEN_EX in captured.out
