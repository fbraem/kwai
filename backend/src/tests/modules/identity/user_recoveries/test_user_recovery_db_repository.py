from datetime import datetime

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_recoveries import (
    UserRecoveryRepository,
    UserRecoveryDbRepository,
    UserRecovery,
    UserRecoveryEntity,
    UserRecoveryNotFoundException,
)
from kwai.modules.identity.users.user import UserEntity, User


@pytest.fixture(scope="module")
def repo(database: Database) -> UserRecoveryRepository:
    """Fixture for creating a user recovery repository."""
    return UserRecoveryDbRepository(database)


@pytest.fixture(scope="module")
def user_recovery(repo: UserRecoveryRepository) -> UserRecoveryEntity:
    """Fixture for creating a user recovery entity."""
    user_recovery = UserRecovery(
        uuid=UniqueId.generate(),
        expiration=LocalTimestamp(timestamp=datetime.utcnow(), timezone="UTC"),
        user=UserEntity(
            id=1,
            domain=User(
                uuid=UniqueId.generate(),
                email=EmailAddress("jigoro.kano@kwai.com"),
                name=Name(first_name="Jigoro", last_name="Kano"),
            ),
        ),
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
