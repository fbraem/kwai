"""Module for defining factory fixtures for the access token entity."""

from kwai.modules.identity.tokens.access_token import AccessTokenEntity


def make_access_token():
    """A factory fixture for an access token."""

    def _make_access_token() -> AccessTokenEntity: ...

    return _make_access_token
