"""Module that implements the reset password use case."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.password import Password
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryRepository,
)
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


class UserRecoveryExpiredException(Exception):
    """Raised when the user recovery is expired."""


class UserRecoveryConfirmedException(Exception):
    """Raised when the user recovery was already used."""


@dataclass(frozen=True, kw_only=True)
class ResetPasswordCommand:
    """Command for the reset password use case.

    Attributes:
        uuid: The unique id of the user recovery
        password: The new password.
    """

    uuid: str
    password: str


class ResetPassword:
    """Reset password use case.

    This use case will try to reset the password of a user. A user can reset the
    password with a unique id. This unique id is linked to a user recovery.
    """

    def __init__(
        self,
        user_account_repo: UserAccountRepository,
        user_recovery_repo: UserRecoveryRepository,
    ):
        """Initialize the use case.

        Args:
            user_account_repo (UserAccountRepository): The repository for getting the
                user account.
            user_recovery_repo (UserRecoveryRepository): The repository for getting and
                updating the user recovery.
        """
        self._user_account_repo = user_account_repo
        self._user_recovery_repo = user_recovery_repo

    async def execute(self, command: ResetPasswordCommand) -> None:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            UserRecoveryNotFoundException: Raised when the user recovery with the
                given uuid does not exist.
            UserRecoveryExpiredException: Raised when the user recovery is expired.
            UserRecoveryConfirmedException: Raised when the user recovery is already
                used.
            UserAccountNotFoundException: Raised when the user with the email address
                that belongs to the user recovery, does not exist.
            NotAllowedException: Raised when the user is revoked.
        """
        user_recovery = await self._user_recovery_repo.get_by_uuid(
            UniqueId.create_from_string(command.uuid)
        )
        if user_recovery.is_expired:
            raise UserRecoveryExpiredException()
        if user_recovery.confirmed:
            raise UserRecoveryConfirmedException()

        user_account = await self._user_account_repo.get_user_by_email(
            user_recovery.user.email
        )

        user_account = user_account.reset_password(
            Password.create_from_string(command.password)
        )
        await self._user_account_repo.update(user_account)

        user_recovery = user_recovery.confirm()
        await self._user_recovery_repo.update(user_recovery)
