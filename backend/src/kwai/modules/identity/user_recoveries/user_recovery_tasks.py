"""Module that defines entry points for tasks for user recoveries."""
from typing import Any

from loguru import logger

from kwai.core.dependencies import create_database, create_mailer, get_template_engine
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.mail.recipient import Recipient, Recipients
from kwai.core.settings import get_settings
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.mail_user_recovery import (
    MailUserRecovery,
    MailUserRecoveryCommand,
)
from kwai.modules.identity.user_recoveries.user_recovery_db_repository import (
    UserRecoveryDbRepository,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryNotFoundException,
)


async def email_user_recovery_task(event: dict[str, Any]):
    """Actor for sending a user recovery mail."""
    logger.info(f"Trying to handle event {event['meta']['name']}")

    settings = get_settings()
    mailer = create_mailer(settings)
    template_engine = get_template_engine(settings)
    database = create_database(settings)

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
