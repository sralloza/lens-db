import pytest

from lens_db.main import get_options


class TestGetOptions:

    class TestNow:
        def test_with_argument(self):
            with pytest.raises(SystemExit):
                get_options('-now 5'.split())

        def test_without_argument(self):
            opt = get_options(['-now'])
            assert 'now' in opt
            assert opt.now is True

    class TestDays:
        def test_with_number(self):
            opt = get_options('-days 5'.split())
            assert 'days' in opt
            assert opt.days == 5

        def test_without_number(self):
            with pytest.raises(SystemExit):
                get_options('-days'.split())

    def test_scan(self):
        opt = get_options('-scan'.split())
        assert 'scan' in opt
        assert opt.scan is True

    def test_last(self):
        opt = get_options('-last'.split())
        assert 'last' in opt
        assert opt.last is True
