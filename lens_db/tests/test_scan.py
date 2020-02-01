from datetime import date, timedelta
from enum import Enum, auto
from unittest import mock

import pytest

from lens_db.src.scanner import scan


class ScanCode(Enum):
    no_entries = auto()
    not_sent = auto()
    day_after_tomorrow = auto()
    tomorrow = auto()
    today = auto()
    expired = auto()


class TestScan:
    @pytest.fixture
    def mocks(self):
        get_last = mock.patch("lens_db.src.scanner.Lens.get_last").start()
        today_date = mock.patch("lens_db.src.scanner.today_date").start()
        send_email = mock.patch("lens_db.src.scanner.send_email").start()

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
