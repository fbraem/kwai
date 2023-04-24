"""Module that defines entry points for tasks for user invitations."""
from typing import Any

from loguru import logger

from kwai.core.db.database import Database
from kwai.core.dependencies import container
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients, Recipient
from kwai.core.settings import Settings
from kwai.core.template.mail_template import MailTemplate
from kwai.core.template.template_engine import TemplateEngine
from kwai.modules.identity.mail_user_invitation import (
    MailUserInvitationCommand,
    MailUserInvitation,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationNotFoundException,
)


async def email_user_invitation_task(event: dict[str, Any]):
    """Task for sending the user invitation email."""
    logger.info(f"Trying to handle event {event['meta']['name']}.")

    mailer = container[Mailer]
    template_engine = container[TemplateEngine]
    database = container[Database]

    command = MailUserInvitationCommand(uuid=event["data"]["uuid"])

    try:
        await MailUserInvitation(
            UserInvitationDbRepository(database),
            mailer,
            Recipients(
                from_=Recipient(
                    email=EmailAddress(container[Settings].website.email),
                    name=container[Settings].website.name,
                )
            ),
            MailTemplate(
                template_engine.create("identity/invitation_html"),
                template_engine.create("identity/invitation_txt"),
            ),
        ).execute(command)
    except UnprocessableException as ex:
        logger.error(f"Task not processed: {ex}")
    except UserInvitationNotFoundException:
        logger.error(
            f"Mail not send because user invitation does not exist "
            f"with uuid {command.uuid}"
        )
