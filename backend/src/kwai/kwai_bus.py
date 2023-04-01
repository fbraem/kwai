"""Entry point for starting the event bus."""
import asyncio
import os
import sys

from loguru import logger
from redis.asyncio import Redis

from kwai.core.dependencies import container
from kwai.core.events.redis_bus import RedisBus
from kwai.core.settings import Settings, SettingsException


def create_bus():
    """Create the event bus."""
    try:
        settings = container[Settings]
    except SettingsException as ex:
        logger.error(f"Could not load settings: {ex}")
        sys.exit(0)

    if settings.redis.logger:
        try:
            logger.remove(0)  # Remove the default logger
        except ValueError:
            pass  # ignore the non-existence of the default logger

    def log_format(record):
        """Create a logging format for an event."""
        new_format = "{time} - {level}"
        if "event_id" in record["extra"]:
            new_format += " - ({extra[event_id]})"
        if "message_id" in record["extra"] and "stream" in record["extra"]:
            new_format += " - ({extra[stream]}: {extra[message_id]})"
        new_format += " - {message}" + os.linesep

        return new_format

    logger.add(
        settings.redis.logger.file or sys.stderr,
        format=log_format,
        level=settings.redis.logger.level,
        colorize=True,
        retention=settings.redis.logger.retention,
        rotation=settings.redis.logger.rotation,
    )

    bus = RedisBus(container[Redis])
    # pylint: disable=(import-outside-toplevel)
    from kwai.modules.identity.tasks import tasks as identity_tasks

    # Subscribe all identity tasks to their event
    for event, task_fn in identity_tasks.items():
        bus.subscribe(event, task_fn)

    return bus


if __name__ == "__main__":
    asyncio.run(create_bus().run())
