"""Module for testing the refresh token entity."""

from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity


def test_create(make_access_token) -> None:
    """Test creation of a refresh token entity."""
    token = RefreshTokenEntity(
        access_token=make_access_token(),
        expiration=Timestamp.create_now().add_delta(days=1),
    )
    assert token.revoked is False, "A new token should not be revoked"
    assert token.expired is False, "A new token should not be expired"
