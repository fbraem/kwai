"""Module for testing the User Log repository for a database."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.user_log import UserLogEntity
from kwai.modules.identity.tokens.user_log_db_repository import UserLogDbRepository
from kwai.modules.identity.tokens.value_objects import IpAddress


pytestmark = pytest.mark.db


async def test_create(database: Database):
    """Test creating a user log in the database."""
    user_log = UserLogEntity(
        success=True,
        email="jigoro.kano@kwai.com",
        client_ip=IpAddress.create("127.0.0.1"),
        user_agent="testclient",
    )

    repo = UserLogDbRepository(database)
    user_log = await repo.create(user_log)
    assert user_log.id is not None
