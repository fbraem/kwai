"""Module to start dramatiq."""
import os
import sys

import dramatiq.brokers.rabbitmq
from dramatiq.middleware import CurrentMessage
from loguru import logger

from kwai.core.dependencies import container
from kwai.core.events.dramatiq_bus import DramatiqBus
from kwai.core.settings import Settings, SettingsException


def create_bus():
    """Wrap the creation of the bus in this method.

    :remark: We must be sure that the @actor decorators are run after setting the
    broker. That's why all actors are imported here.
    """
    try:
        settings = container[Settings]
    except SettingsException as ex:
        logger.error(f"Could not load settings: {ex}")
        sys.exit(0)

    if settings.broker.logger:
        try:
            logger.remove(0)  # Remove the default logger
        except ValueError:
            pass

        def log_format(record):
            """Create a logging format for a message."""
            if (
                "message_id" in record["extra"]
                and "actor_name" in record["extra"]
                and "queue_name" in record["extra"]
            ):
                return (
                    "{time} - {level} - "
                    "({extra[message_id]} - "
                    "{extra[actor_name]} - "
                    "{extra[queue_name]}) - "
                    "{message}" + os.linesep
                )
            return "{time} - {level} - {message}" + os.linesep

        logger.add(
            settings.broker.logger.file or sys.stderr,
            format=log_format,
            level=settings.broker.logger.level,
            colorize=True,
            retention=settings.broker.logger.retention,
            rotation=settings.broker.logger.rotation,
        )

    broker = dramatiq.brokers.rabbitmq.RabbitmqBroker(
        url=settings.broker.url + "/" + settings.broker.name
    )
    broker.add_middleware(CurrentMessage())
    dramatiq.set_broker(broker)

    bus = DramatiqBus()

    # pylint: disable=(import-outside-toplevel)
    from kwai.modules.identity.tasks import tasks as identity_tasks

    # Subscribe all identity tasks to their event
    for event, task_fn in identity_tasks.items():
        bus.subscribe(event, task_fn)

    return bus


if __name__ == "__main__":
    create_bus()
