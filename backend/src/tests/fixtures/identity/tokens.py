"""Module for defining factory fixtures for token entities."""

import pytest

from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture
def make_access_token(make_user_account):
    """A factory fixture for an access token."""

    def _make_access_token(
        identifier: TokenIdentifier | None = None,
        expiration: Timestamp | None = None,
        user_account: UserAccountEntity | None = None,
    ) -> AccessTokenEntity:
        return AccessTokenEntity(
            identifier=identifier or TokenIdentifier.generate(),
            expiration=expiration or Timestamp.create_with_delta(minutes=10),
            user_account=user_account or make_user_account(),
        )

    return _make_access_token


@pytest.fixture
def make_access_token_in_db(
    request, event_loop, database, make_access_token, make_user_account_in_db
):
    """Factory fixture for creating an access token in database."""

    async def _make_access_token_in_db(
        access_token: AccessTokenEntity | None = None,
        user_account: UserAccountEntity | None = None,
    ) -> AccessTokenEntity:
        if access_token is None:
            access_token = make_access_token(
                user_account=user_account or await make_user_account_in_db()
            )
        repo = AccessTokenDbRepository(database)

        async with UnitOfWork(database):
            access_token = await repo.create(access_token)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(access_token)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return access_token

    return _make_access_token_in_db


@pytest.fixture
def make_refresh_token(make_access_token):
    """A factory fixture for refresh token."""

    def _make_refresh_token(
        access_token: AccessTokenEntity | None = None,
        identifier: TokenIdentifier | None = None,
        expiration: Timestamp | None = None,
    ) -> RefreshTokenEntity:
        return RefreshTokenEntity(
            access_token=access_token or make_access_token(),
            identifier=identifier or TokenIdentifier.generate(),
            expiration=expiration or Timestamp.create_with_delta(minutes=10),
        )

    return _make_refresh_token


@pytest.fixture
def make_refresh_token_in_db(
    request, event_loop, database, make_access_token_in_db, make_refresh_token
):
    """Factory fixture for creating a refresh token in database."""

    async def _make_refresh_token_in_db(
        refresh_token: RefreshTokenEntity | None = None,
    ) -> RefreshTokenEntity:
        if refresh_token is None:
            refresh_token = make_refresh_token(
                access_token=await make_access_token_in_db()
            )
        repo = RefreshTokenDbRepository(database)

        async with UnitOfWork(database):
            access_token = await repo.create(refresh_token)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(access_token)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return access_token

    return _make_refresh_token_in_db
