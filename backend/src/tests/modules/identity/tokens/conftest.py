"""Module that defines fixtures for testing identity tokens."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token_repository import RefreshTokenRepository


@pytest.fixture(scope="module")
def access_token_repo(database: Database) -> AccessTokenRepository:
    """Fixture for creating an access token repository."""
    return AccessTokenDbRepository(database)


@pytest.fixture(scope="module")
def refresh_token_repo(database: Database) -> RefreshTokenRepository:
    """Fixture for creating the refresh token repository."""
    return RefreshTokenDbRepository(database)
