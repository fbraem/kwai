"""Module with tests for the access token database repository."""
from datetime import datetime

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture(scope="module")
def repo(database: Database) -> AccessTokenRepository:
    """Fixture for creating the repository."""
    return AccessTokenDbRepository(database)


@pytest.fixture(scope="module")
def access_token(
    repo: AccessTokenRepository, user_account: UserAccountEntity
) -> AccessTokenEntity:
    """Fixture for creating an access token."""
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=datetime.utcnow(),
        user_account=user_account,
    )

    return repo.create(token)


def test_create(
    access_token: AccessTokenEntity,  # pylint: disable=redefined-outer-name
):
    """Test the creation of an access_token."""
    assert access_token.id, "There should be an access token entity"


def test_get_by_token_identifier(
    repo: AccessTokenRepository,  # pylint: disable=redefined-outer-name
    access_token: AccessTokenEntity,  # pylint: disable=redefined-outer-name
):
    """Test get_by_token_identifier."""
    token = repo.get_by_identifier(access_token.identifier)
    assert token, "There should be a refresh token"


def test_query(
    repo: AccessTokenRepository,  # pylint: disable=redefined-outer-name
):
    """Test query."""
    tokens = list(repo.get_all(limit=10))
    assert len(tokens) > 0, "There should be at least 1 token"
