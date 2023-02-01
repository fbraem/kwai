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
def user_recovery(repo: UserRecoveryRepository, user: UserEntity) -> UserRecoveryEntity:
    """Fixture for creating a user recovery entity."""
    user_recovery = UserRecoveryEntity(
        expiration=LocalTimestamp(timestamp=datetime.utcnow(), timezone="UTC"),
        user=user,
    )
    return repo.create(user_recovery)


def test_create(user_recovery: UserRecoveryEntity):
    """Test if the user recovery was created."""
    assert user_recovery.id, "There should be a user recovery created"


def test_get_by_uuid(repo: UserRecoveryRepository, user_recovery: UserRecoveryEntity):
    """Test if the user recovery can be fetched with the uuid."""
    recovery = repo.get_by_uuid(user_recovery.uuid)
    assert recovery, "There should be a recovery with the given uuid"


def test_update(repo: UserRecoveryRepository, user_recovery: UserRecoveryEntity):
    """Test if the user recovery can be updated."""
    user_recovery.confirm()
    repo.update(user_recovery)
    recovery = repo.get_by_uuid(user_recovery.uuid)
    assert recovery.confirmation, "There should be a confirmation date"


def test_delete(repo: UserRecoveryRepository, user_recovery: UserRecoveryEntity):
    """Test if the user recovery can be deleted."""
    repo.delete(user_recovery)

    with pytest.raises(UserRecoveryNotFoundException):
        repo.get_by_uuid(user_recovery.uuid)
