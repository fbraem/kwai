"""Module that implements the recover user use case."""
from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.events.bus import Bus
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
        _event_bus (Bus): An event bus for dispatching the UserRecoveryCreatedEvent
            event.
    """

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        user_repo: UserAccountRepository,
        user_recovery_repo: UserRecoveryRepository,
        event_bus: Bus,
    ):
        self._user_account_repo = user_repo
        self._user_recovery_repo = user_recovery_repo
        self._event_bus = event_bus

    async def execute(self, command: RecoverUserCommand) -> UserRecoveryEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            UserAccountNotFoundException: Raised when the user with the given email
                address does not exist.
            UnprocessableException: Raised when the user is revoked
        """
        user_account = self._user_account_repo.get_user_by_email(
            EmailAddress(command.email)
        )
        if user_account.revoked:
            raise UnprocessableException("User account is revoked")

        user_recovery = self._user_recovery_repo.create(
            UserRecoveryEntity(
                user=user_account.user,
                expiration=LocalTimestamp.create_with_delta(hours=2),
            )
        )

        await self._event_bus.publish(
            UserRecoveryCreatedEvent(uuid=str(user_recovery.uuid))
        )

        return user_recovery
