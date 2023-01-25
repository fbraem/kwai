"""Module with tests for the access token database repository."""
from datetime import datetime

import pytest

from kwai.core.db import Database
from kwai.core.domain.value_objects import UniqueId, EmailAddress, Name
from kwai.core.domain.value_objects.password import Password
from kwai.modules.identity.tokens.access_token_db_repository import (
    AccessTokenDbRepository,
)
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users import User, UserAccountEntity, UserAccount


@pytest.fixture(scope="module")
def repo(database: Database) -> AccessTokenRepository:
    """Fixture for creating the repository."""
    return AccessTokenDbRepository(database)


@pytest.fixture(scope="module")
def access_token(
    repo: AccessTokenRepository,  # pylint: disable=redefined-outer-name
) -> AccessTokenEntity:
    """Fixture for creating an access token."""
    token = AccessTokenEntity(
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
    )

    return repo.create(token)


def test_create(
    access_token: AccessTokenEntity,  # pylint: disable=redefined-outer-name
):
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
