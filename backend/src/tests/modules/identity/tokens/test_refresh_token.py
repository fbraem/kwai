"""Module for testing the refresh token entity."""

import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture
def access_token() -> AccessTokenEntity:
    """Fixture for an access token entity."""
    return AccessTokenEntity(
        user_account=UserAccountEntity(
            password=Password.create_from_string("Test1234"),
            user=UserEntity(
                uuid=UniqueId.generate(),
                name=Name(first_name="Jigoro", last_name="Kano"),
                email=EmailAddress("jigoro.kano@kwai.com"),
            ),
        )
    )


def test_create(access_token: AccessTokenEntity) -> None:
    """Test creation of a refresh token entity."""
    token = RefreshTokenEntity(
        access_token=access_token,
        expiration=Timestamp.create_now().add_delta(days=1),
    )
    assert token.revoked is False, "A new token should not be revoked"
    assert token.expired is False, "A new token should not be expired"
