"""Module for starting the event bus."""

import asyncio
import os
import sys

from typing import Any

from faststream import BaseMiddleware, FastStream
from faststream.redis import RedisBroker, RedisRouter
from faststream.security import SASLPlaintext
from loguru import logger

from kwai.core.settings import LoggerSettings, get_settings
from kwai.events.v1 import router as v1_router


class LoggerMiddleware(BaseMiddleware):
    """Middleware that adds logging to the event bus."""

    async def on_consume(self, msg: Any) -> Any:
        """Set up a context for the logger."""
        with logger.contextualize():
            return await super().on_consume(msg)


def configure_logger(logger_settings: LoggerSettings):
    """Configure the logger."""
    try:
        logger.remove(0)  # Remove the default logger
    except ValueError:
        pass

    def log_format(record):
        """Change the format when a request_id is set in extra."""
        if "event_id" in record["extra"]:
            new_format = (
                "{time} - {level} - ({extra[event_id]}) - {message}" + os.linesep
            )
        else:
            new_format = "{time} - {level} - {message}" + os.linesep
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


settings = get_settings()

broker = RedisBroker(
    url=f"redis://{settings.redis.host}:{settings.redis.port}",
    middlewares=[LoggerMiddleware],
    security=SASLPlaintext(
        username="",
        password=settings.redis.password,
    ),
)
router = RedisRouter(prefix="kwai/")
router.include_router(v1_router)
broker.include_router(router)


async def main():
    """Start the event bus."""
    app = FastStream(broker)
    await app.run()


asyncio.run(main())
