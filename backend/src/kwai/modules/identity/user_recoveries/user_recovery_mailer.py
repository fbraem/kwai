"""Module that defines a mailer for a user recovery email."""
from kwai.core.domain.mailer_service import MailerService
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.message import Message
from kwai.core.mail.recipient import Recipients, Recipient
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.user_recoveries import UserRecoveryEntity


class UserRecoveryMailer(MailerService):
    """Sends a user recovery mail."""

    def __init__(
        self,
        mailer: Mailer,
        recipients: Recipients,
        mail_template: MailTemplate,
        user_recovery: UserRecoveryEntity,
    ):
        self._mailer = mailer
        self._recipients = recipients
        self._mail_template = mail_template
        self._user_recovery = user_recovery

    def send(self) -> Message:
        template_vars = {
            "uuid": str(self._user_recovery.uuid),
            "name": str(self._user_recovery.user.name),
            "expires": 2,
        }

        mail = self._mail_template.create_mail(
            self._recipients.with_to(
                Recipient(
                    email=self._user_recovery.user.email,
                    name=str(self._user_recovery.user.name),
                )
            ),
            "User recovery",
            **template_vars,
        )

        self._mailer.send(mail)

        return mail
