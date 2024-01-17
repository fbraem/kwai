"""Module for defining the event application."""
import asyncio
import os
import sys

from loguru import logger
from redis.asyncio import Redis

from kwai.core.events.redis_bus import RedisBus
from kwai.core.settings import LoggerSettings, get_settings

settings = get_settings()


def configure_logger(logger_settings: LoggerSettings):
    """Configure the logger."""
    try:
        logger.remove(0)  # Remove the default logger
    except ValueError:
        pass

    def log_format(record):
        """Change the format when a request_id is set in extra."""
        new_format = "{time} - {level}"
        if "stream" in record["extra"]:
            new_format += " - {extra[stream]}"
        if "message_id" in record["extra"]:
            new_format += " - ({extra[message_id]})"
        new_format += " - {message}" + os.linesep
        if record["exception"]:
            new_format += "{exception}" + os.linesep
        return new_format

    logger.add(
        logger_settings.file or sys.stderr,
        format=log_format,
        level=logger_settings.level,
        colorize=True,
        retention=logger_settings.retention,
        rotation=logger_settings.rotation,
        backtrace=False,
        diagnose=False,
    )


redis = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
)

bus = RedisBus(redis)
asyncio.run(bus.run())
