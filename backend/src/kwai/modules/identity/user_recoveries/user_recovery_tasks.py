"""Module that defines entry points for tasks for user recoveries."""
from dramatiq import actor
from loguru import logger

from kwai.core.events.logging_actor import LoggingActor


@actor(actor_name="identity.user_recovery.email", actor_class=LoggingActor)
def email_user_recovery_task(event):
    """Actor for creating a user recovery mail."""
    logger.info(event)
