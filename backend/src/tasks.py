import os
import sys

from loguru import logger

from kwai.core.events import CeleryBus
from kwai.core.events.celery import get_celery_app
from kwai.core.settings import get_settings, SettingsException
from kwai.modules.identity.user_recoveries.user_recovery_events import (
    UserRecoveryCreatedEvent,
)
from kwai.modules.identity.user_recoveries.user_recovery_tasks import (
    EmailUserRecoveryTask,
)

settings = None
try:
    settings = get_settings()
except SettingsException as se:
    logger.error(f"Could not load the settings: {se}!")
    exit(1)

app = get_celery_app(settings.celery)

if settings.celery.logger:
    logger.remove()  # Remove the default logger

    def log_format(record):
        if "task_id" in record["extra"] and "task_name" in record["extra"]:
            return (
                "{time} - {level} - ({extra[task_id]} - {extra[task_name]}) - {message}"
                + os.linesep
            )
        return "{time} - {level} - {message}" + os.linesep

    logger.add(
        settings.celery.logger.file or sys.stderr,
        format=log_format,
        level=settings.celery.logger.level,
        colorize=True,
        retention=settings.celery.logger.retention,
        rotation=settings.celery.logger.rotation,
    )

celery_bus = CeleryBus(app)
celery_bus.subscribe(UserRecoveryCreatedEvent, EmailUserRecoveryTask())
