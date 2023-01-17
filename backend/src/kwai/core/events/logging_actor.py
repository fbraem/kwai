"""Module that defines an actor that provides context information to the logger."""
from dramatiq import Actor
from dramatiq.middleware import CurrentMessage
from loguru import logger


class LoggingActor(Actor):
    """A base actor that makes message_id, actor_name and queue_name available to the logger."""

    def __call__(self, *args, **kwargs):
        """Add a logger context for an actor."""
        message = CurrentMessage.get_current_message()
        with logger.contextualize(
            message_id=message.message_id,
            actor_name=message.actor_name,
            queue_name=message.queue_name,
        ):
            return super().__call__(*args, **kwargs)
