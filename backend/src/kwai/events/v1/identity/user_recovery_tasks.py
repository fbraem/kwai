"""Module that defines entry points for tasks for user recoveries."""
from typing import Any

from fast_depends import Depends
from faststream.redis import RedisRouter
from loguru import logger

from kwai.api.dependencies import create_database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.events.dependencies import create_mailer, create_template_engine
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
from kwai.modules.identity.user_recoveries.user_recovery_events import (
    UserRecoveryCreatedEvent,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryNotFoundException,
)

router = RedisRouter()


@router.subscriber(stream=UserRecoveryCreatedEvent.meta.name)
async def email_user_recovery_task(
    event: dict[str, Any],
    settings=Depends(get_settings),
    database=Depends(create_database),
    mailer=Depends(create_mailer),
    template_engine=Depends(create_template_engine),
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
