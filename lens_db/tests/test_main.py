from argparse import Namespace
from unittest import mock

import pytest

from lens_db.src.exceptions import BaseLensDBError
from lens_db.src.main import _main, get_options, main


def modified_get_options(string: str):
    return get_options(string.split())


class TestGetOptions:
    class TestNow:
        def test_with_argument(self):
            with pytest.raises(SystemExit):
                modified_get_options("-now 5")

        def test_without_argument(self):
            opt = modified_get_options("-now")
            assert "now" in opt
            assert opt.now is True

    class TestDays:
        def test_with_number(self):
            opt = modified_get_options("-days 5")
            assert "days" in opt
            assert opt.days == 5

        def test_without_number(self):
            with pytest.raises(SystemExit):
                modified_get_options("-days")

    def test_scan(self):
        opt = modified_get_options("-scan")
        assert "scan" in opt
        assert opt.scan is True

    def test_last(self):
        opt = modified_get_options("-last")
        assert "last" in opt
        assert opt.last is True

    class TestFromStr:
        def test_with_argument(self):
            opt = get_options(["-from-str", "some old string"])
            assert "from_str" in opt
            assert opt.from_str == "some old string"

        def test_without_argument(self):
            with pytest.raises(SystemExit):
                modified_get_options("-from-str")

    def test_list(self):
        opt = modified_get_options("-list")
        assert "list" in opt
        assert opt.list is True


@mock.patch("lens_db.src.main.scan")
@mock.patch("lens_db.src.main.get_options")
@mock.patch("lens_db.src.main.Lens")
class TestHiddenMain:
    def test_scan(self, lens_mock, options_mock, scan_mock):
        options_mock.return_value = Namespace(
            days=None, from_str=None, last=False, list=False, now=False, scan=True
        )
        _main()

        scan_mock.assert_called_once_with()
        lens_mock.add.assert_not_called()
        lens_mock.add_custom.assert_not_called()
        lens_mock.list.assert_not_called()
        lens_mock.get_last.assert_not_called()

    def test_days(self, lens_mock, options_mock, scan_mock):
        options_mock.return_value = Namespace(
            days=5, from_str=None, last=False, list=False, now=False, scan=False
        )

        _main()

        scan_mock.assert_not_called()
        lens_mock.add.assert_called_once_with(delta_days=5)
        lens_mock.add_custom.assert_not_called()
        lens_mock.list.assert_not_called()
        lens_mock.get_last.assert_not_called()

    def test_now(self, lens_mock, options_mock, scan_mock):
        options_mock.return_value = Namespace(
            days=None, from_str=None, last=False, list=False, now=True, scan=False
        )
        _main()

        scan_mock.assert_not_called()
        lens_mock.add.assert_called_once_with(delta_days=0)
        lens_mock.add_custom.assert_not_called()
        lens_mock.list.assert_not_called()
        lens_mock.get_last.assert_not_called()

    def test_from_str(self, lens_mock, options_mock, scan_mock):
        options_mock.return_value = Namespace(
            days=None,
            from_str="some-str",
            last=False,
            list=False,
            now=False,
            scan=False,
        )
        _main()

        scan_mock.assert_not_called()
        lens_mock.add.assert_not_called()
        lens_mock.add_custom.assert_called_once_with("some-str")
        lens_mock.list.assert_not_called()
        lens_mock.get_last.assert_not_called()

    def test_list(self, lens_mock, options_mock, scan_mock):
        options_mock.return_value = Namespace(
            days=None, from_str=None, last=False, list=True, now=False, scan=False
        )

        with pytest.raises(SystemExit):
            _main()

        scan_mock.assert_not_called()
        lens_mock.add.assert_not_called()
        lens_mock.add_custom.assert_not_called()
        lens_mock.list.assert_called_once_with()
        lens_mock.get_last.assert_not_called()

    def test_last(self, lens_mock, options_mock, scan_mock):
        options_mock.return_value = Namespace(
            days=None, from_str=None, last=True, list=False, now=False, scan=False
        )

        with pytest.raises(SystemExit):
            _main()

        scan_mock.assert_not_called()
        lens_mock.add.assert_not_called()
        lens_mock.add_custom.assert_not_called()
        lens_mock.list.assert_not_called()
        lens_mock.get_last.assert_called_once_with()


    def test_last_empty(self, lens_mock, options_mock, scan_mock):
        options_mock.return_value = Namespace(
            days=None, from_str=None, last=True, list=False, now=False, scan=False
        )

        lens_mock.get_last.return_value = None

        with pytest.raises(SystemExit, match="No lens"):
            _main()

        scan_mock.assert_not_called()
        lens_mock.add.assert_not_called()
        lens_mock.add_custom.assert_not_called()
        lens_mock.list.assert_not_called()
        lens_mock.get_last.assert_called_once_with()


@mock.patch("lens_db.src.main._main")
class TestRealMain:
    def test_normal(self, hidden_main_mock):
        main()
        hidden_main_mock.assert_called_once_with()

    @mock.patch("lens_db.src.main.exception_exit")
    def test_error(self, exc_exit_mock, hidden_main_mock):
        exc = BaseLensDBError("exc")
        hidden_main_mock.side_effect = exc

        main()
        exc_exit_mock.assert_called_once_with(exc)
