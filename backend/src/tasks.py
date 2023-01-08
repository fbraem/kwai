import os
import sys

from loguru import logger
from kombu import Queue, Exchange

from kwai.core.events.celery import get_celery_app
from kwai.core.settings import get_settings, SettingsException

_QUEUES = ("kwai", "identity")

app = get_celery_app()
app.conf.task_create_missing_queues = False
app.conf.task_queues = (
    Queue(name=q, exchange=Exchange("q"), routing_key=q) for q in _QUEUES
)
app.conf.task_default_queue = "kwai"
app.conf.task_routes = {
    "identity.*": {"queue": "identity"},
}

settings = None
try:
    settings = get_settings()
except SettingsException as se:
    logger.error(f"Could not load the settings: {se}!")
    exit(1)

if settings.celery.logger:
    logger.remove(0)  # Remove the default logger

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
