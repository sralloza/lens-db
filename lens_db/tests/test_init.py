from unittest import mock


def test_logging_setup():
    lm = mock.patch('logging.basicConfig').start()
    import lens_db
    del lens_db

    lm.assert_called_once()

    mock.patch.stopall()