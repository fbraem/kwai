"""Module for testing the refresh token entity."""


def test_create(make_refresh_token) -> None:
    """Test creation of a refresh token entity."""
    token = make_refresh_token()
    assert token.revoked is False, "A new token should not be revoked"
    assert token.expired is False, "A new token should not be expired"
