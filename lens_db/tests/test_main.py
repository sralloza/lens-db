from argparse import Namespace
from unittest import mock

import pytest

import lens_db
from lens_db.src.exceptions import BaseLensDBError
from lens_db.src.main import _main, get_options, main


def modified_get_options(string: str):
    return get_options(string.split())


class TestGetOptions:
    class TestNow:
        def test_with_argument(self):
            with pytest.raises(SystemExit):
                modified_get_options("now 5")

        def test_without_argument(self):
            opt = modified_get_options("now")
            assert opt.command == "now"

    class TestDays:
        def test_with_number(self):
            opt = modified_get_options("days 5")
            assert opt.command == "days"
            assert opt.days == 5

        def test_without_number(self):
            with pytest.raises(SystemExit):
                modified_get_options("days")

    def test_scan(self):
        opt = modified_get_options("scan")
        assert opt.command == "scan"

    def test_last(self):
        opt = modified_get_options("last")
        assert opt.command == "last"

    class TestFromStr:
        def test_with_argument(self):
            opt = get_options(["from-str", "some old string"])
            assert opt.command == "from-str"
            assert opt.string == "some old string"

        def test_without_argument(self):
            with pytest.raises(SystemExit):
                modified_get_options("from-str")

    def test_list(self):
        opt = modified_get_options("list")
        assert opt.command == "list"

    class TestCredentials:
        def test_ok_normal(self):
            opt = get_options(["credentials", "user", "pass"])
            assert opt.command == "credentials"
            assert opt.username == "user"
            assert opt.password == "pass"

        def test_ok_special(self):
            opt = get_options(["credentials", "--", "-user-", "-pass-"])
            assert opt.command == "credentials"
            assert opt.username == "-user-"
            assert opt.password == "-pass-"

        def test_no_username(self):
            with pytest.raises(SystemExit):
                get_options(["credentials", "-pass-"])

        def test_no_args(self):
            with pytest.raises(SystemExit):
                get_options(["credentials"])

    def test_disable(self):
        opt = get_options(["disable"])
        assert opt.command == "disable"

    def test_enable(self):
        opt = get_options(["enable"])
        assert opt.command == "enable"

    def test_status(self):
        opt = get_options(["status"])
        assert opt.command == "status"


class TestHiddenMain:
    @pytest.fixture
    def mocks(self):
        scan_m = mock.patch("lens_db.src.main.scan").start()
        options_m = mock.patch("lens_db.src.main.get_options").start()
        lens_m = mock.patch("lens_db.src.main.Lens").start()
        creds_m = mock.patch("lens_db.src.main.save_credentials").start()
        dis_m = mock.patch("lens_db.src.main.disable").start()
        en_m = mock.patch("lens_db.src.main.enable").start()
        st_m = mock.patch("lens_db.src.main.show_status").start()

        yield scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m

        mock.patch.stopall()

    def test_scan(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(command="scan")
        _main()

        scan_m.assert_called_once_with()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_not_called()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_not_called()
        st_m.assert_not_called()

    def test_days(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(days=5, command="days")

        _main()

        scan_m.assert_not_called()
        lens_m.add.assert_called_once_with(delta_days=5)
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_not_called()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_not_called()
        st_m.assert_not_called()

    def test_now(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(command="now")
        _main()

        scan_m.assert_not_called()
        lens_m.add.assert_called_once_with(delta_days=0)
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_not_called()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_not_called()
        st_m.assert_not_called()

    def test_from_str(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(string="some-str", command="from-str")
        _main()

        scan_m.assert_not_called()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_called_once_with("some-str")
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_not_called()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_not_called()
        st_m.assert_not_called()

    def test_list(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(command="list")

        with pytest.raises(SystemExit):
            _main()

        scan_m.assert_not_called()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_called_once_with()
        lens_m.get_last.assert_not_called()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_not_called()
        st_m.assert_not_called()

    def test_last(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(command="last")

        with pytest.raises(SystemExit):
            _main()

        scan_m.assert_not_called()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_called_once_with()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_not_called()
        st_m.assert_not_called()

    def test_last_empty(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(command="last")

        lens_m.get_last.return_value = None

        with pytest.raises(SystemExit, match="No lens"):
            _main()

        scan_m.assert_not_called()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_called_once_with()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_not_called()
        st_m.assert_not_called()

    def test_credentials(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(
            command="credentials", username="-user-", password="-pass-"
        )

        _main()

        scan_m.assert_not_called()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_not_called()
        creds_m.assert_called_once_with(username="-user-", password="-pass-")

    def test_disable(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(command="disable")

        _main()

        scan_m.assert_not_called()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_not_called()
        creds_m.assert_not_called()
        dis_m.assert_called()
        en_m.assert_not_called()
        st_m.assert_not_called()

    def test_enable(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(command="enable")

        _main()

        scan_m.assert_not_called()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_not_called()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_called()
        st_m.assert_not_called()

    def test_show_status(self, mocks):
        scan_m, options_m, lens_m, creds_m, dis_m, en_m, st_m = mocks
        options_m.return_value = Namespace(command="status")

        _main()

        scan_m.assert_not_called()
        lens_m.add.assert_not_called()
        lens_m.add_custom.assert_not_called()
        lens_m.list.assert_not_called()
        lens_m.get_last.assert_not_called()
        creds_m.assert_not_called()
        dis_m.assert_not_called()
        en_m.assert_not_called()
        st_m.assert_called()


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
