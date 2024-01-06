"""Module for defining the faststream application."""
import os
import sys

from faststream import BaseMiddleware, FastStream
from faststream.rabbit import RabbitBroker
from faststream.types import DecodedMessage
from loguru import logger

from kwai.core.settings import LoggerSettings, get_settings
from kwai.events.v1 import router

settings = get_settings()


class LoggerMiddleware(BaseMiddleware):
    """Middleware for setting up logger."""

    async def on_consume(self, msg: DecodedMessage) -> DecodedMessage:
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


if settings.rabbitmq.logger:
    configure_logger(settings.rabbitmq.logger)
    middlewares = [LoggerMiddleware]
else:
    middlewares = []


broker = RabbitBroker(
    host=settings.rabbitmq.host,
    port=settings.rabbitmq.port,
    login=settings.rabbitmq.user,
    password=settings.rabbitmq.password,
    virtualhost=settings.rabbitmq.vhost,
    middlewares=middlewares,
)
broker.include_router(router)
app = FastStream(broker)
