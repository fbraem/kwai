"""Module that implements the use case: authenticate user."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.exceptions import AuthenticationException
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.access_token_repository import AccessTokenRepository
from kwai.modules.identity.tokens.log_user_login_service import LogUserLoginService
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.tokens.refresh_token_repository import RefreshTokenRepository
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


@dataclass(kw_only=True, frozen=True)
class AuthenticateUserCommand:
    """Input for the (AuthenticateUser) use case.

    Attributes:
        username: The email address of the user.
        password: The password of the user.
        access_token_expiry_minutes: Minutes before expiring the access token.
            Default is 2 hours.
        refresh_token_expiry_minutes: Minutes before expiring the refresh token.
            Default is 2 months.
    """

    username: str
    password: str | None = None
    access_token_expiry_minutes: int = 60 * 2  # 2 hours
    refresh_token_expiry_minutes: int = 60 * 24 * 60  # 2 months


class AuthenticateUser:
    """Use case to authenticate a user."""

    def __init__(
        self,
        user_account_repo: UserAccountRepository,
        access_token_repo: AccessTokenRepository,
        refresh_token_repo: RefreshTokenRepository,
        log_user_login_service: LogUserLoginService,
    ):
        self._user_account_repo = user_account_repo
        self._access_token_repo = access_token_repo
        self._refresh_token_repo = refresh_token_repo
        self._log_user_login_service = log_user_login_service

    async def execute(self, command: AuthenticateUserCommand) -> RefreshTokenEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Returns:
            RefreshTokenEntity: On success, a refresh token entity will be returned.

        Raises:
            InvalidEmailException: Raised when the username
                contains an invalid email address.
            UserAccountNotFoundException: Raised when the user with the given email
                address doesn't exist.
        """
        user_account = await self._user_account_repo.get_user_by_email(
            EmailAddress(command.username)
        )
        if user_account.revoked:
            # save the last unsuccessful login
            await self._user_account_repo.update(user_account)

            message = "User account is revoked"
            await self._log_user_login_service.notify_failure(
                message, user_account=user_account
            )
            raise AuthenticationException(message)

        user_account = user_account.login(command.password)
        if not user_account.logged_in:
            # save the last unsuccessful login
            await self._user_account_repo.update(user_account)

            message = "Invalid password"
            await self._log_user_login_service.notify_failure(
                message, user_account=user_account
            )
            raise AuthenticationException(message)

        access_token = await self._access_token_repo.create(
            AccessTokenEntity(
                expiration=Timestamp.create_with_delta(
                    minutes=command.access_token_expiry_minutes
                ),
                user_account=user_account,
            )
        )

        refresh_token = await self._refresh_token_repo.create(
            RefreshTokenEntity(
                expiration=Timestamp.create_with_delta(
                    minutes=command.refresh_token_expiry_minutes
                ),
                access_token=access_token,
            )
        )

        # save the last successful login
        await self._user_account_repo.update(user_account)

        await self._log_user_login_service.notify_success(
            user_account=user_account, refresh_token=refresh_token
        )

        return refresh_token
