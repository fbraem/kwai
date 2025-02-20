"""Module that defines the use case for refreshing an access token."""

from dataclasses import dataclass

from kwai.modules.identity.authenticate_user import AuthenticationException
from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository
from kwai.modules.identity.tokens.log_user_login_service import LogUserLoginService
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

    def __init__(
        self,
        refresh_token_repo: RefreshTokenRepository,
        access_token_repo: AccessTokenRepository,
        log_user_login_service: LogUserLoginService,
    ):
        self._refresh_token_repo = refresh_token_repo
        self._access_token_repo = access_token_repo
        self._log_user_login_service = log_user_login_service

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
            message = "Refresh token is expired"
            await self._log_user_login_service.notify_failure(
                message,
                user_account=refresh_token.access_token.user_account,
                refresh_token=refresh_token,
            )
            raise AuthenticationException(message)

        if refresh_token.revoked:
            message = "Refresh token is revoked"
            await self._log_user_login_service.notify_failure(
                message,
                user_account=refresh_token.access_token.user_account,
                refresh_token=refresh_token,
            )
            raise AuthenticationException(message)

        # When the user is revoked, revoke the access and refresh tokens.
        if refresh_token.access_token.user_account.revoked:
            refresh_token.revoke()
            await self._refresh_token_repo.update(refresh_token)
            # The access token is also revoked, so update it
            await self._access_token_repo.update(refresh_token.access_token)

            message = "User is revoked"
            await self._log_user_login_service.notify_failure(
                message,
                user_account=refresh_token.access_token.user_account,
                refresh_token=refresh_token,
            )
            raise AuthenticationException(message)

        # Renew the refresh token
        refresh_token = refresh_token.renew(
            command.refresh_token_expiry_minutes, command.access_token_expiry_minutes
        )

        await self._refresh_token_repo.update(refresh_token)
        await self._access_token_repo.update(refresh_token.access_token)

        return refresh_token
