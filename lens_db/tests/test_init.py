from unittest import mock

import pytest


@pytest.mark.xfail
@mock.patch('logging.basicConfig')
def test_logging_setup(lm):
    from lens_db import logging
    del logging

    lm.assert_called_once()
