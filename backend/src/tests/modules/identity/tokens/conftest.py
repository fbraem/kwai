"""Module that defines fixtures for testing identity tokens."""
from datetime import datetime

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.access_token import (
    AccessTokenEntity,
)
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token_repository import RefreshTokenRepository
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture(scope="module")
def access_token_repo(database: Database) -> AccessTokenRepository:
    """Fixture for creating an access token repository."""
    return AccessTokenDbRepository(database)


@pytest.fixture(scope="module")
def access_token(
    access_token_repo: AccessTokenRepository, user_account: UserAccountEntity
) -> AccessTokenEntity:
    """Fixture for creating an access token."""
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=datetime.utcnow(),
        user_account=user_account,
    )

    return access_token_repo.create(token)


@pytest.fixture(scope="module")
def refresh_token_repo(database: Database) -> RefreshTokenRepository:
    """Fixture for creating the refresh token repository."""
    return RefreshTokenDbRepository(database)


@pytest.fixture(scope="module")
def refresh_token(
    refresh_token_repo: RefreshTokenRepository, access_token: AccessTokenEntity
) -> RefreshTokenEntity:
    """Fixture for creating a refresh token."""
    token = RefreshTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=datetime.utcnow(),
        access_token=access_token,
    )
    return refresh_token_repo.create(token)
