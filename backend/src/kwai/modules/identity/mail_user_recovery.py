"""Module that defines the use case for sending a recovery email."""

from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.user_recoveries.user_recovery_mailer import (
    UserRecoveryMailer,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryRepository,
)


@dataclass(frozen=True, kw_only=True)
class MailUserRecoveryCommand:
    """Command for the use case MailUserRecovery.

    Attributes:
        uuid: The unique id of the user recovery.
    """

    uuid: str


class MailUserRecovery:
    """Use case for sending a recovery email."""

    def __init__(
        self,
        user_recovery_repo: UserRecoveryRepository,
        mailer: Mailer,
        recipients: Recipients,
        mail_template: MailTemplate,
    ):
        self._user_recovery_repo = user_recovery_repo
        self._mailer = mailer
        self._recipients = recipients
        self._mail_template = mail_template

    async def execute(self, command: MailUserRecoveryCommand) -> UserRecoveryEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.

        Raises:
            UserRecoveryNotFoundException: Raised when
                the user recovery cannot be found.
            UnprocessableException: Raised when the mail was already sent.
                Raised when the user recovery was already confirmed.
        """
        user_recovery = await self._user_recovery_repo.get_by_uuid(
            UniqueId.create_from_string(command.uuid)
        )

        if user_recovery.mailed:
            raise UnprocessableException(
                f"Mail already send for user recovery {command.uuid}"
            )

        if user_recovery.is_expired:
            raise UnprocessableException(
                f"User recovery {command.uuid} already expired"
            )

        if user_recovery.confirmed:
            raise UnprocessableException(
                f"User recovery {command.uuid} already confirmed"
            )

        UserRecoveryMailer(
            self._mailer, self._recipients, self._mail_template, user_recovery
        ).send()

        user_recovery.mail_sent()

        await self._user_recovery_repo.update(user_recovery)

        return user_recovery
