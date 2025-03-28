"""Module for defining the event application."""

import asyncio
import os
import signal
import sys

import inject

from loguru import logger
from redis.asyncio import Redis

from kwai.core.events import dependencies
from kwai.core.events.redis_bus import RedisBus
from kwai.core.settings import LoggerSettings, Settings
from kwai.events.v1 import router


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


def shutdown(sig, frame):
    """A signal has been received to stop the application."""
    print(f"Received exit signal {signal.Signals(sig).name}")
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()


@inject.autoparams()
async def main(settings: Settings):
    """Main program."""
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
    )

    if settings.redis.logger:
        configure_logger(settings.redis.logger)

    bus = RedisBus(redis)
    for route_element in router:
        bus.subscribe(route_element)

    for sig in (signal.SIGINT, signal.SIGTERM):
        asyncio.get_running_loop().add_signal_handler(sig, shutdown, sig, None)

    logger.info("Starting the event bus.")
    await bus.run()


if __name__ == "__main__":
    dependencies.configure()
    asyncio.run(main())
    logger.info("The bus has stopped!")
