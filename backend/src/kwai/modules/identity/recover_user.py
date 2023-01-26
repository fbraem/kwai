"""Module that implements the recover user use case."""
from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.core.events.bus import Bus
from kwai.modules.identity.user_recoveries import (
    UserRecoveryEntity,
    UserRecoveryRepository,
    UserRecovery,
)
from kwai.modules.identity.user_recoveries.user_recovery_events import (
    UserRecoveryCreatedEvent,
)
from kwai.modules.identity.users.user_account_repository import UserAccountRepository


@dataclass(frozen=True, kw_only=True)
class RecoverUserCommand:
    """Command for the recover user use case."""

    email: str


class RecoverUser:
    """Use case: recover user."""

    def __init__(
        self,
        user_repo: UserAccountRepository,
        user_recovery_repo: UserRecoveryRepository,
        event_bus: Bus,
    ):
        self._user_account_repo = user_repo
        self._user_recovery_repo = user_recovery_repo
        self._event_bus = event_bus

    def execute(self, command: RecoverUserCommand) -> UserRecoveryEntity:
        """Executes the use case.

        :raises:
            kwai.modules.identity.users.user_repository.UserAccountNotFoundException:
                Raised when the user with the given email address does not exist.
            kwai.core.domain.exceptions.UnprocessableException:
                Raised when the user is revoked
        """
        user_account = self._user_account_repo.get_user_by_email(
            EmailAddress(command.email)
        )
        if user_account.revoked:
            raise UnprocessableException("User account is revoked")

        user_recovery = self._user_recovery_repo.create(
            UserRecovery(
                uuid=UniqueId.generate(),
                user=user_account.user,
                expiration=LocalTimestamp.create_future(hours=2),
            )
        )

        self._event_bus.publish(UserRecoveryCreatedEvent(uuid=str(user_recovery.uuid)))

        return user_recovery
