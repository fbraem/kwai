"""Module that defines tests for user recovery database."""
from datetime import datetime

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.user_recoveries.user_recovery_db_repository import (
    UserRecoveryDbRepository,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryNotFoundException,
    UserRecoveryRepository,
)
from kwai.modules.identity.users.user import UserEntity

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def repo(database: Database) -> UserRecoveryRepository:
    """Fixture for creating a user recovery repository."""
    return UserRecoveryDbRepository(database)


@pytest.fixture(scope="module")
async def user_recovery(
    repo: UserRecoveryRepository, user: UserEntity
) -> UserRecoveryEntity:
    """Fixture for creating a user recovery entity."""
    user_recovery = UserRecoveryEntity(
        expiration=LocalTimestamp(timestamp=datetime.utcnow(), timezone="UTC"),
        user=user,
    )
    return await repo.create(user_recovery)


def test_create(user_recovery: UserRecoveryEntity):
    """Test if the user recovery was created."""
    assert user_recovery.id, "There should be a user recovery created"


@pytest.mark.asyncio
async def test_get_by_uuid(
    repo: UserRecoveryRepository, user_recovery: UserRecoveryEntity
):
    """Test if the user recovery can be fetched with the uuid."""
    recovery = await repo.get_by_uuid(user_recovery.uuid)
    assert recovery, "There should be a recovery with the given uuid"


@pytest.mark.asyncio
async def test_update(repo: UserRecoveryRepository, user_recovery: UserRecoveryEntity):
    """Test if the user recovery can be updated."""
    user_recovery.confirm()
    await repo.update(user_recovery)
    recovery = await repo.get_by_uuid(user_recovery.uuid)
    assert recovery.confirmed_at, "There should be a confirmation date"


@pytest.mark.asyncio
async def test_delete(repo: UserRecoveryRepository, user_recovery: UserRecoveryEntity):
    """Test if the user recovery can be deleted."""
    await repo.delete(user_recovery)

    with pytest.raises(UserRecoveryNotFoundException):
        await repo.get_by_uuid(user_recovery.uuid)
