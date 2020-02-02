import pytest

from lens_db.src.main import get_options


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
