"""Module for defining factory fixtures for token entities."""

import pytest

from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture
def make_access_token(make_user_account):
    """A factory fixture for an access token."""

    def _make_access_token(
        identifier: TokenIdentifier | None = None,
        expiration: Timestamp | None = None,
        user_account: UserAccountEntity | None = None,
    ) -> AccessTokenEntity:
        return AccessTokenEntity(
            identifier=identifier,
            expiration=expiration,
            user_account=user_account or make_user_account(),
        )

    return _make_access_token


@pytest.fixture
def make_refresh_token(make_access_token):
    """A factory fixture for refresh token."""

    def _make_refresh_token(
        access_token: AccessTokenEntity | None = None,
        identifier: TokenIdentifier | None = None,
        expiration: Timestamp | None = None,
    ) -> RefreshTokenEntity:
        return RefreshTokenEntity(
            access_token=access_token or make_access_token(),
            identifier=identifier,
            expiration=expiration,
        )

    return _make_refresh_token
