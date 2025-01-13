"""Module that defines tests for user recovery database."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.user_recoveries.user_recovery_db_repository import (
    UserRecoveryDbRepository,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryNotFoundException,
    UserRecoveryRepository,
)


pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> UserRecoveryRepository:
    """Fixture for creating a user recovery repository."""
    return UserRecoveryDbRepository(database)


async def test_create(make_user_recovery, repo: UserRecoveryRepository) -> None:
    """Test if the user recovery was created."""
    user_recovery = make_user_recovery()
    user_recovery = await repo.create(user_recovery)
    assert user_recovery.id, "There should be a user recovery created"


async def test_get_by_uuid(repo: UserRecoveryRepository, make_user_recovery_in_db):
    """Test if the user recovery can be fetched with the uuid."""
    user_recovery = await make_user_recovery_in_db()
    recovery = await repo.get_by_uuid(user_recovery.uuid)
    assert recovery, "There should be a recovery with the given uuid"


async def test_update(repo: UserRecoveryRepository, make_user_recovery_in_db):
    """Test if the user recovery can be updated."""
    user_recovery = await make_user_recovery_in_db()
    user_recovery = user_recovery.confirm()
    await repo.update(user_recovery)
    recovery = await repo.get_by_uuid(user_recovery.uuid)
    assert not recovery.confirmation.empty, "There should be a confirmation date"
    assert recovery.confirmed, "The user recovery should be a confirmed"


async def test_delete(repo: UserRecoveryRepository, make_user_recovery_in_db):
    """Test if the user recovery can be deleted."""
    user_recovery = await make_user_recovery_in_db()
    await repo.delete(user_recovery)

    with pytest.raises(UserRecoveryNotFoundException):
        await repo.get_by_uuid(user_recovery.uuid)
