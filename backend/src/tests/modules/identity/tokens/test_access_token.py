"""Module for testing the access token entity."""

import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture
def account() -> UserAccountEntity:
    """Fixture for account entity."""
    return UserAccountEntity(
        password=Password.create_from_string("Test1234"),
        user=UserEntity(
            uuid=UniqueId.generate(),
            name=Name(first_name="Jigoro", last_name="Kano"),
            email=EmailAddress("jigoro.kano@kwai.com"),
        ),
    )


def test_create(account: UserAccountEntity) -> None:
    """Test creation of an access token."""
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=Timestamp.create_now(),
        user_account=account,
    )

    assert token.revoked is False, "A new token should not be revoked."


def test_expired(account: UserAccountEntity) -> None:
    """Test if an access token is expired."""
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=Timestamp.create_now(),
        user_account=account,
    )

    assert token.expired is True, "The token should be expired."


def test_not_expired(account: UserAccountEntity) -> None:
    """Test if an access token is not expired."""
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=Timestamp.create_now().add_delta(days=1),
        user_account=account,
    )

    assert token.expired is False, "The token should not be expired."
