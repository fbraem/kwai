"""Module that defines a mailer for a user invitation."""
from kwai.core.domain.mailer_service import MailerService
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.message import Message
from kwai.core.mail.recipient import Recipients, Recipient
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity


class UserInvitationMailer(MailerService):
    """Send a user invitation mail."""

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        mailer: Mailer,
        recipients: Recipients,
        mail_template: MailTemplate,
        user_invitation: UserInvitationEntity,
    ):
        self._mailer = mailer
        self._recipients = recipients
        self._mail_template = mail_template
        self._user_invitation = user_invitation

    def send(self) -> Message:
        template_vars = {
            "uuid": str(self._user_invitation.uuid),
            "name": str(self._user_invitation.name),
            "expires": 2,
        }

        mail = self._mail_template.create_mail(
            self._recipients.with_to(
                Recipient(
                    email=self._user_invitation.email,
                    name=str(self._user_invitation.user.name),
                )
            ),
            "User invitation",
            **template_vars,
        )

        self._mailer.send(mail)

        return mail
