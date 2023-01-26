"""Module for testing the refresh token database repository."""
from datetime import datetime

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.tokens.access_token import (
    AccessTokenIdentifier,
    AccessTokenEntity,
)
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.refresh_token_db_repository import (
    RefreshTokenDbRepository,
)
from kwai.modules.identity.tokens.refresh_token_repository import RefreshTokenRepository
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture(scope="module")
def repo(database: Database) -> RefreshTokenRepository:
    """Fixture for creating the repository."""
    return RefreshTokenDbRepository(database)


@pytest.fixture(scope="module")
def refresh_token(
    repo: RefreshTokenRepository,  # pylint: disable=redefined-outer-name
) -> RefreshTokenEntity:
    """Fixture for creating a refresh token."""
    token = RefreshTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=datetime.utcnow(),
        access_token=AccessTokenEntity(
            id=AccessTokenIdentifier(1),
            user_account=UserAccountEntity(
                password=Password.create_from_string("Test1234"),
                user=UserEntity(
                    email=EmailAddress("jigoro.kano@kwai.com"),
                    name=Name(first_name="Jigoro", last_name="Kano"),
                ),
            ),
        ),
    )
    return repo.create(token)


def test_create(
    refresh_token: RefreshTokenEntity,  # pylint: disable=redefined-outer-name
):
    """Test the create method."""
    assert not refresh_token.id.is_empty(), "There should be a refresh token entity"


def test_get_by_token_identifier(
    repo: RefreshTokenRepository,  # pylint: disable=redefined-outer-name
    refresh_token: RefreshTokenEntity,  # pylint: disable=redefined-outer-name
):
    """Test get_by_token_identifier."""
    token = repo.get_by_token_identifier(refresh_token.identifier)
    assert token, "There should be a refresh token"


def test_query(
    repo: RefreshTokenRepository,  # pylint: disable=redefined-outer-name
):
    """Test query."""
    tokens = list(repo.get_all(limit=10))
    assert len(tokens) > 0, "There should be at least 1 token"
