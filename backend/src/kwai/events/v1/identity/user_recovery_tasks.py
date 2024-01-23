"""Module that defines entry points for tasks for user recoveries."""
from typing import Any

import inject
from loguru import logger

from kwai.core.db.database import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.events.event_router import EventRouter
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipient, Recipients
from kwai.core.settings import Settings
from kwai.core.template.mail_template import MailTemplate
from kwai.core.template.template_engine import TemplateEngine
from kwai.modules.identity.mail_user_recovery import (
    MailUserRecovery,
    MailUserRecoveryCommand,
)
from kwai.modules.identity.user_recoveries.user_recovery_db_repository import (
    UserRecoveryDbRepository,
)
from kwai.modules.identity.user_recoveries.user_recovery_events import (
    UserRecoveryCreatedEvent,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryNotFoundException,
)


@inject.autoparams()
async def email_user_recovery_task(
    event: dict[str, Any],
    settings: Settings,
    database: Database,
    mailer: Mailer,
    template_engine: TemplateEngine,
):
    """Actor for sending a user recovery mail."""
    command = MailUserRecoveryCommand(uuid=event["data"]["uuid"])

    try:
        await MailUserRecovery(
            UserRecoveryDbRepository(database),
            mailer,
            Recipients(
                from_=Recipient(
                    email=EmailAddress(settings.website.email),
                    name=settings.website.name,
                )
            ),
            MailTemplate(
                template_engine.create("identity/recover_html"),
                template_engine.create("identity/recover_txt"),
            ),
        ).execute(command)
    except UnprocessableException as ex:
        logger.error(f"Task not processed: {ex}")
    except UserRecoveryNotFoundException:
        logger.error(
            f"Mail not send because user recovery does not exist "
            f"with uuid {command.uuid}"
        )


router = (
    EventRouter(event=UserRecoveryCreatedEvent, callback=email_user_recovery_task),
)
