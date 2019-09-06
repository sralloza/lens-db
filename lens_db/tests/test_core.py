from datetime import date
from pathlib import Path
from unittest import mock

import pytest

from lens_db.core import Lens, DBConnection
from lens_db.exceptions import InvalidDateError

DATABASE_PATH = Path(__file__).parent.parent / 'lens.db'


class TestModuleAttributes:
    def test_database_path(self):
        from lens_db.core import DATABASE_PATH
        assert isinstance(DATABASE_PATH, Path)
        assert DATABASE_PATH.name == 'lens.db'


class TestLens:
    days_str = (
        (4, '2019-12-27'),
        (6, '2019-12-25'),
        (9, '2019-12-22'),
        (10, '2019-12-21'),
        (16, '2019-12-15'),
        (20, '2019-12-11'),
    )

    @pytest.mark.parametrize('days, day_str', days_str)
    @mock.patch('lens_db.core.today_date', return_value=date(2019, 12, 31))
    @mock.patch('lens_db.core.Lens.add_custom')
    def test_add(self, add_custom, today_date, days, day_str):
        Lens.add(days)
        today_date.assert_called_once_with()
        add_custom.assert_called_once_with(day_str)

    add_custom_data = (

        ('2019-12-27', True),
        ('2019-12-25', True),
        ('2019-12-22', True),
        ('2019-12-21', True),
        ('2019.12.15', False),
        ('15-12-2019', False),
        ('20191211', False),
        ('Whatever', False)
    )

    @pytest.mark.parametrize('date_str, is_ok', add_custom_data)
    @mock.patch('lens_db.core.DBConnection')
    def test_add_custom(self, db_mock, date_str, is_ok):
        if is_ok:
            Lens.add_custom(date_str)
        else:
            with pytest.raises(InvalidDateError):
                Lens.add_custom(date_str)
            return

        db_mock.assert_called()
        db_mock.return_value.__enter__.assert_called()
        db_mock.return_value.__enter__.return_value.add.assert_called_once_with(date_str)
        db_mock.return_value.__exit__.assert_called()

    get_last_data = (
        ('2019-12-27', date(2019, 12, 27)),
        ('2019-12-25', date(2019, 12, 25)),
        ('2019-12-22', date(2019, 12, 22)),
        ('2019-12-21', date(2019, 12, 21)),
        ('2019-12-15', date(2019, 12, 15)),
        ('2019-12-11', date(2019, 12, 11)),
        (None, None)
    )

    @pytest.mark.parametrize('date_returned, expected', get_last_data)
    @mock.patch('lens_db.core.DBConnection')
    def test_get_last(self, db_mock, date_returned, expected):
        db_mock.return_value.__enter__.return_value.get_last.return_value = date_returned

        last = Lens.get_last()
        assert expected == last

        db_mock.assert_called()
        db_mock.return_value.__enter__.assert_called()
        db_mock.return_value.__enter__.return_value.get_last.assert_called_once_with()
        db_mock.return_value.__exit__.assert_called()


class TestDBConnection:

    @mock.patch('lens_db.core.DBConnection.ensure_table')
    @mock.patch('sqlite3.connect')
    def test_init(self, connect_mock, table_mock):
        DBConnection()

        connect_mock.assert_called()
        connect_mock.return_value.cursor.assert_called_once()
        table_mock.assert_called_once()

    @mock.patch('lens_db.core.DBConnection.commit')
    @mock.patch('lens_db.core.DBConnection.close')
    @mock.patch('sqlite3.connect')
    def test_context_manager(self, connect_mock, close_mock, commit_mock):
        assert hasattr(DBConnection, '__enter__')
        assert hasattr(DBConnection, '__exit__')

        with DBConnection():
            pass

        connect_mock.assert_called()
        close_mock.assert_called()
        commit_mock.assert_called()

    @mock.patch('sqlite3.connect')
    def test_enter(self, connect_mock):
        connection = DBConnection()
        enter = connection.__enter__()

        assert connection == enter
        connect_mock.assert_called()

    @mock.patch('lens_db.core.DBConnection.commit')
    @mock.patch('lens_db.core.DBConnection.close')
    @mock.patch('sqlite3.connect')
    def test_exit(self, connect_mock, close_mock, commit_mock):
        connection = DBConnection()
        connection.__exit__(None, None, None)

        connect_mock.assert_called()
        close_mock.assert_called()
        commit_mock.assert_called()

    @mock.patch('sqlite3.connect')
    def test_commit(self, connect_mock):
        connection = DBConnection()
        connection.commit()

        connect_mock.return_value.commit.assert_called()

    @mock.patch('sqlite3.connect')
    def test_close(self, connect_mock):
        cursor_mock = connect_mock.return_value.cursor

        connection = DBConnection()
        connection.close()

        connect_mock.return_value.close.assert_called_once()
        cursor_mock.return_value.close.assert_called_once()

    @mock.patch('sqlite3.connect')
    def test_ensure_table(self, connect_mock):
        connection = DBConnection()
        connection.ensure_table()

        cursor = connect_mock.return_value.cursor
        call_arg = cursor.return_value.execute.call_args[0][0]

        assert "CREATE TABLE IF NOT EXISTS 'lens'" in call_arg
        assert 'id' in call_arg
        assert 'timestamp' in call_arg

    @mock.patch('sqlite3.connect')
    def test_add(self, connect_mock):
        connection = DBConnection()
        connection.add('hello')

        cursor = connect_mock.return_value.cursor
        cursor.return_value.execute.assert_called_with('INSERT INTO lens VALUES (NULL, ?)',
                                                       ['hello'])

    @pytest.mark.parametrize('full', [True, False])
    @mock.patch('sqlite3.connect')
    def test_get_last(self, connect_mock, full):
        cursor = connect_mock.return_value.cursor

        if full:
            cursor.return_value.fetchall.return_value = [['2019-10-02'], ['2019-01-01'],
                                                         ['2018-02-02']]
        else:
            cursor.return_value.fetchall.side_effect = TypeError

        connection = DBConnection()
        last = connection.get_last()

        if full:
            assert last == '2018-02-02'
        else:
            assert last is None

        cursor.return_value.execute.assert_called_with(
            'SELECT timestamp FROM lens ORDER BY timestamp')
