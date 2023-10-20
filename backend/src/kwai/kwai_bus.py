"""Entry point for starting the event bus."""
import asyncio
import os
import sys

from fastapi import Depends
from loguru import logger

from kwai.core.dependencies import create_redis
from kwai.core.events.redis_bus import RedisBus
from kwai.core.settings import Settings, get_settings


def create_bus(settings: Settings = Depends(get_settings)):
    """Create the event bus."""
    redis = create_redis(settings)

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

    bus = RedisBus(redis)

    from kwai.modules.identity.tasks import tasks as identity_tasks

    # Subscribe all identity tasks to their event
    for event, task_fn in identity_tasks.items():
        bus.subscribe(event, task_fn)

    return bus


if __name__ == "__main__":
    settings = get_settings()
    asyncio.run(create_bus(settings).run())
