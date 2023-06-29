"""Module that defines the use case for refreshing an access token."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from kwai.modules.identity.authenticate_user import AuthenticationException
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.refresh_token_repository import RefreshTokenRepository
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshAccessTokenCommand:
    """Input for the refresh access token use case.

    Attributes:
        identifier: The identifier of the refresh token.
        access_token_expiry_minutes: Minutes before expiring the access token.
            Default is 2 hours.
        refresh_token_expiry_minutes: Minutes before expiring the refresh token.
            Default is 2 months.
    """

    identifier: str  # The identifier of the refresh token.
    access_token_expiry_minutes: int = 60 * 2  # 2 hours
    refresh_token_expiry_minutes: int = 60 * 24 * 60  # 2 months


class RefreshAccessToken:
    """Use case for refreshing an access token.

    Attributes:
        _refresh_token_repo (RefreshTokenRepository): The repo for getting and creating
            a new refresh token.
        _access_token_repo (AccessTokenRepository): The repo for updating and creating
            an access token.

    Note:
        A new access token will also result in a new refresh token.
    """

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        refresh_token_repo: RefreshTokenRepository,
        access_token_repo: AccessTokenRepository,
    ):
        self._refresh_token_repo = refresh_token_repo
        self._access_token_repo = access_token_repo

    async def execute(self, command: RefreshAccessTokenCommand) -> RefreshTokenEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            RefreshTokenNotFoundException: Raised when the refresh token does not exist.
            AuthenticationException: Raised when the refresh token is expired, the
                refresh token is revoked or the user is revoked.
        """
        refresh_token = await self._refresh_token_repo.get_by_token_identifier(
            TokenIdentifier(hex_string=command.identifier)
        )

        if refresh_token.expired:
            raise AuthenticationException("Refresh token is expired")

        if refresh_token.revoked:
            raise AuthenticationException("Refresh token is revoked")

        # Revoke the old refresh token and access token
        refresh_token.revoke()
        await self._refresh_token_repo.update(refresh_token)
        # The access token is also revoked, so update it
        await self._access_token_repo.update(refresh_token.access_token)

        if refresh_token.access_token.user_account.revoked:
            raise AuthenticationException("User is revoked")

        # Create a new access and refresh token
        access_token = await self._access_token_repo.create(
            AccessTokenEntity(
                identifier=TokenIdentifier.generate(),
                expiration=datetime.utcnow()
                + timedelta(minutes=command.access_token_expiry_minutes),
                user_account=refresh_token.access_token.user_account,
            )
        )

        return await self._refresh_token_repo.create(
            RefreshTokenEntity(
                identifier=TokenIdentifier.generate(),
                expiration=datetime.utcnow()
                + timedelta(minutes=command.refresh_token_expiry_minutes),
                access_token=access_token,
            )
        )
