"""Module that implements the use case: authenticate user."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from kwai.core.domain.value_objects import EmailAddress
from kwai.modules.identity import AuthenticationException
from kwai.modules.identity.tokens import (
    RefreshTokenRepository,
    AccessTokenRepository,
    TokenIdentifier,
)
from kwai.modules.identity.tokens.access_token import AccessTokenEntity
from kwai.modules.identity.tokens.refresh_token import RefreshTokenEntity
from kwai.modules.identity.users import UserAccountRepository


@dataclass(kw_only=True, frozen=True)
class AuthenticateUserCommand:
    """Input for the AuthenticateUser use case."""

    username: str
    password: str
    access_token_expiry_minutes: int = 60 * 2  # 2 hours
    refresh_token_expiry_minutes: int = 60 * 24 * 60  # 2 months


class AuthenticateUser:
    """Authenticate user.

    A refresh token will be returned when the user is successfully authenticated.
    """

    def __init__(
        self,
        user_account_repo: UserAccountRepository,
        access_token_repo: AccessTokenRepository,
        refresh_token_repo: RefreshTokenRepository,
    ):
        self._user_account_repo = user_account_repo
        self._access_token_repo = access_token_repo
        self._refresh_token_repo = refresh_token_repo

    def execute(self, command: AuthenticateUserCommand) -> RefreshTokenEntity:
        """Executes the use case.

        :raises:
            core.domain.value_objects.InvalidEmailException: Raised when the username contains an invalid email address.
        :raises:
            UserAccountNotFoundException: Raised when the user with the given email address doesn't exist.
        """
        user_account = self._user_account_repo.get_user_by_email(
            EmailAddress(command.username)
        )
        if user_account().revoked:
            raise AuthenticationException("User account is revoked")

        if not user_account().login(command.password):
            self._user_account_repo.update(
                user_account
            )  # save the last unsuccessful login
            raise AuthenticationException("Invalid password")

        self._user_account_repo.update(user_account)  # save the last successful login

        access_token = self._access_token_repo.create(
            AccessTokenEntity(
                identifier=TokenIdentifier.generate(),
                expiration=datetime.utcnow()
                + timedelta(minutes=command.access_token_expiry_minutes),
                user_account=user_account,
            )
        )

        return self._refresh_token_repo.create(
            RefreshTokenEntity(
                identifier=TokenIdentifier.generate(),
                expiration=datetime.utcnow()
                + timedelta(minutes=command.refresh_token_expiry_minutes),
                access_token=access_token,
            )
        )
