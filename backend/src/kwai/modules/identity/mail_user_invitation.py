"""Module that defines the use case for sending a user invitation email."""
from dataclasses import dataclass

from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_mailer import (
    UserInvitationMailer,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)


@dataclass(frozen=True, kw_only=True, slots=True)
class MailUserInvitationCommand:
    """Command for the use case MailUserInvitation.

    Attributes:
        uuid: The unique id of the user invitation.
    """

    uuid: str


class MailUserInvitation:
    """Use case for sending a user invitation email."""

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        user_invitation_repo: UserInvitationRepository,
        mailer: Mailer,
        recipients: Recipients,
        mail_template: MailTemplate,
    ):
        self._user_invitation_repo = user_invitation_repo
        self._mailer = mailer
        self._recipients = recipients
        self._mail_template = mail_template

    def execute(self, command: MailUserInvitationCommand) -> UserInvitationEntity:
        """Executes the use case.

        Args:
            command: the input for this use case.
        Raises:
            UserInvitationNotFoundException: Raised when
                the user invitation cannot be found.
            UnprocessableException: Raised when the mail was already sent.
                Raised when the user recovery was already confirmed.
        """
        user_invitation = self._user_invitation_repo.get_invitation_by_uuid(
            UniqueId.create_from_string(command.uuid)
        )
        if user_invitation.mailed:
            raise UnprocessableException(
                f"Mail already send for user invitation {command.uuid}"
            )

        if user_invitation.is_expired:
            raise UnprocessableException(
                f"User invitation {command.uuid} already expired"
            )

        if user_invitation.confirmed:
            raise UnprocessableException(
                f"User invitation {command.uuid} already confirmed"
            )

        UserInvitationMailer(
            self._mailer,
            self._recipients,
            self._mail_template,
            user_invitation,
        ).send()

        user_invitation.mail_sent()

        return user_invitation
