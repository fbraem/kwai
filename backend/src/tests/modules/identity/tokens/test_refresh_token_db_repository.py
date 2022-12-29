"""Module for testing the refresh token database repository."""
from datetime import datetime

import pytest

from kwai.core.db import Database
from kwai.core.domain.value_objects import EmailAddress, Name, UniqueId, Password
from kwai.modules.identity.tokens import (
    AccessTokenEntity,
    AccessToken,
    RefreshToken,
    RefreshTokenEntity,
    RefreshTokenDbRepository,
    RefreshTokenRepository,
    TokenIdentifier,
)
from kwai.modules.identity.users import User, UserAccountEntity, UserAccount


@pytest.fixture(scope="module")
def repo(database: Database) -> RefreshTokenRepository:
    """Fixture for creating the repository."""
    return RefreshTokenDbRepository(database)


@pytest.fixture(scope="module")
def refresh_token(
    repo: RefreshTokenRepository,  # pylint: disable=redefined-outer-name
) -> RefreshTokenEntity:
    """Fixture for creating a refresh token."""
    token = RefreshToken(
        identifier=TokenIdentifier.generate(),
        expiration=datetime.utcnow(),
        access_token=AccessTokenEntity(
            id=1,
            domain=AccessToken(
                identifier=TokenIdentifier.generate(),
                expiration=datetime.utcnow(),
                user_account=UserAccountEntity(
                    id=1,
                    domain=UserAccount(
                        password=Password.create_from_string("Test1234"),
                        user=User(
                            uuid=UniqueId.generate(),
                            email=EmailAddress("jigoro.kano@kwai.com"),
                            name=Name(first_name="Jigoro", last_name="Kano"),
                        ),
                    ),
                ),
            ),
        ),
    )
    return repo.create(token)


def test_create(
    refresh_token: RefreshTokenEntity,  # pylint: disable=redefined-outer-name
):
    """Test the create method."""
    assert refresh_token.id, "There should be a refresh token entity"


def test_get_by_token_identifier(
    repo: RefreshTokenRepository,  # pylint: disable=redefined-outer-name
    refresh_token: RefreshTokenEntity,  # pylint: disable=redefined-outer-name
):
    """Test get_by_token_identifier."""
    token = repo.get_by_token_identifier(refresh_token().identifier)
    assert token, "There should be a refresh token"


def test_query(
    repo: RefreshTokenRepository,  # pylint: disable=redefined-outer-name
):
    """Test query."""
    tokens = list(repo.get_all(limit=10))
    assert len(tokens) > 0, "There should be at least 1 token"
