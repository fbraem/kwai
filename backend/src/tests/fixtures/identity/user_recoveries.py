"""Module for defining factory fixtures for the user recovery entities."""

import pytest

from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.user_recoveries.user_recovery_db_repository import (
    UserRecoveryDbRepository,
)
from kwai.modules.identity.users.user import UserEntity


@pytest.fixture
def make_user_recovery(make_user):
    """Factory fixture for a user recovery entity."""

    def _make_user_recovery(
        expiration: Timestamp | None = None, user: UserEntity | None = None
    ) -> UserRecoveryEntity:
        user_recovery = UserRecoveryEntity(
            expiration=expiration or Timestamp.create_now(),
            user=user or make_user(),
        )
        return user_recovery

    return _make_user_recovery


@pytest.fixture
def make_user_recovery_in_db(
    request, event_loop, database, make_user_recovery, make_user_account_in_db
):
    """Factory fixture for a user recovery entity in database."""

    async def _make_user_recovery_in_db(
        user_recovery: UserRecoveryEntity | None = None,
        user: UserEntity | None = None,
    ) -> UserRecoveryEntity:
        user = user or await make_user_account_in_db()
        user_recovery = user_recovery or make_user_recovery(user=user)
        repo = UserRecoveryDbRepository(database)

        async with UnitOfWork(database):
            user_recovery = await repo.create(user_recovery)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(user_recovery)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return user_recovery

    return _make_user_recovery_in_db
