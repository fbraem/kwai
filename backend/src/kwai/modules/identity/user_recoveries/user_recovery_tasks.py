"""Module that defines entry points for tasks for user recoveries."""
from typing import Any

from dramatiq import actor
from loguru import logger

from kwai.core.db import Database
from kwai.core.dependencies import container
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects import EmailAddress
from kwai.core.events.logging_actor import LoggingActor
from kwai.core.mail import Recipients, Recipient, Mailer
from kwai.core.settings import Settings
from kwai.core.template import TemplateEngine
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.mail_user_recovery import (
    MailUserRecovery,
    MailUserRecoveryCommand,
)
from kwai.modules.identity.user_recoveries import (
    UserRecoveryDbRepository,
    UserRecoveryNotFoundException,
)


@actor(actor_name="identity.user_recovery.email", actor_class=LoggingActor)
def email_user_recovery_task(event: dict[str, Any]):
    """Actor for sending a user recovery mail."""
    logger.info(f"Trying to handle event {event['meta']['name']}")

    mailer = container[Mailer]
    template_engine = container[TemplateEngine]
    database = container[Database]
    database.connect()

    command = MailUserRecoveryCommand(uuid=event["data"]["uuid"])

    try:
        MailUserRecovery(
            UserRecoveryDbRepository(database),
            mailer,
            Recipients(
                from_=Recipient(
                    email=EmailAddress(container[Settings].website.email),
                    name=container[Settings].website.name,
                )
            ),
            MailTemplate(
                template_engine.create("identity/recover_html"),
                template_engine.create("identity/recover_txt"),
            ),
        ).execute(command)
    except UnprocessableException as ue:
        logger.error(f"Task not processed: {ue}")
    except UserRecoveryNotFoundException:
        logger.error(
            f"Mail not send because user recovery does not exist with uuid {command.uuid}"
        )
