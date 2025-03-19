"""Module that defines entry points for tasks for user invitations."""

from typing import Any

import inject

from loguru import logger

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.events.event_router import EventRouter
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipient, Recipients
from kwai.core.settings import Settings
from kwai.core.template.mail_template import MailTemplate
from kwai.core.template.template_engine import TemplateEngine
from kwai.modules.identity.mail_user_invitation import (
    MailUserInvitation,
    MailUserInvitationCommand,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_events import (
    UserInvitationCreatedEvent,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationNotFoundException,
)


@inject.autoparams()
async def email_user_invitation_task(
    event: dict[str, Any],
    settings: Settings,
    database: Database,
    mailer: Mailer,
    template_engine: TemplateEngine,
):
    """Task for sending the user invitation email."""
    command = MailUserInvitationCommand(uuid=event["data"]["uuid"])

    try:
        async with UnitOfWork(database):
            await MailUserInvitation(
                UserInvitationDbRepository(database),
                mailer,
                Recipients(
                    from_=Recipient(
                        email=EmailAddress(settings.website.email),
                        name=settings.website.name,
                    )
                ),
                MailTemplate(
                    template_engine.create("mail/identity/invitation_html"),
                    template_engine.create("mail/identity/invitation_txt"),
                ),
            ).execute(command)
    except UnprocessableException as ex:
        logger.error(f"Task not processed: {ex}")
    except UserInvitationNotFoundException:
        logger.error(
            f"Mail not send because user invitation does not exist "
            f"with uuid {command.uuid}"
        )


router = (
    EventRouter(event=UserInvitationCreatedEvent, callback=email_user_invitation_task),
)
