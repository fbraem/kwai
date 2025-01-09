"""Module for testing the access token entity."""

from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


def test_create(make_user_account) -> None:
    """Test creation of an access token."""
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=Timestamp.create_now(),
        user_account=make_user_account(),
    )

    assert token.revoked is False, "A new token should not be revoked."


def test_expired(make_user_account) -> None:
    """Test if an access token is expired."""
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=Timestamp.create_now(),
        user_account=make_user_account(),
    )

    assert token.expired is True, "The token should be expired."


def test_not_expired(make_user_account) -> None:
    """Test if an access token is not expired."""
    token = AccessTokenEntity(
        identifier=TokenIdentifier.generate(),
        expiration=Timestamp.create_now().add_delta(days=1),
        user_account=make_user_account(),
    )

    assert token.expired is False, "The token should not be expired."
