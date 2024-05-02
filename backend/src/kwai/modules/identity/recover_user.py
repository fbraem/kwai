"""Module that implements the recover user use case."""

from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.events.publisher import Publisher
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.user_recoveries.user_recovery_events import (
    UserRecoveryCreatedEvent,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryRepository,
)
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


@dataclass(frozen=True, kw_only=True)
class RecoverUserCommand:
    """Command for the recover user use case."""

    email: str


class RecoverUser:
    """Use case: recover user.

    Attributes:
        _user_account_repo (UserAccountRepository): The repository for getting the
            user account.
        _user_recovery_repo (UserRecoveryRepository): The repository for creating a
            user recovery.
        _publisher (Bus): An event bus for dispatching the UserRecoveryCreatedEvent
            event.
    """

    def __init__(
        self,
        user_repo: UserAccountRepository,
        user_recovery_repo: UserRecoveryRepository,
        publisher: Publisher,
    ):
        self._user_account_repo = user_repo
        self._user_recovery_repo = user_recovery_repo
        self._publisher = publisher

    async def execute(self, command: RecoverUserCommand) -> UserRecoveryEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            UserAccountNotFoundException: Raised when the user with the given email
                address does not exist.
            UnprocessableException: Raised when the user is revoked
        """
        user_account = await self._user_account_repo.get_user_by_email(
            EmailAddress(command.email)
        )
        if user_account.revoked:
            raise UnprocessableException("User account is revoked")

        user_recovery = await self._user_recovery_repo.create(
            UserRecoveryEntity(
                user=user_account.user,
                expiration=Timestamp.create_with_delta(hours=2),
            )
        )

        await self._publisher.publish(
            UserRecoveryCreatedEvent(uuid=str(user_recovery.uuid))
        )

        return user_recovery
