"""Module for sharing fixtures in this module."""
import pytest

from kwai.core.db import Database
from kwai.core.settings import get_settings


@pytest.fixture(scope="module")
def database():
    """Fixture for getting a connected database."""
    database = Database(get_settings().db)  # pylint: disable=redefined-outer-name
    database.connect()
    return database
