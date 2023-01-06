"""Module that configures Celery."""
from abc import ABC

from celery import Celery, Task
from loguru import logger

from kwai.core.settings import get_settings


class EventTask(Task, ABC):
    """Base class for a task that handles an event."""

    def __call__(self, *args, **kwargs):
        with logger.contextualize(task_id=self.request.id, task_name=self.request.task):
            logger.info(f"{self.request.task}: start")
            try:
                self.run(*args, **kwargs)
                logger.info(f"{self.request.task}: ended")
            except Exception as exc:
                logger.error(f"{self.request.task} failed: {exc}")
                raise


settings = get_settings()


def get_celery_app():
    """Returns a Celery instance."""
    return Celery("kwai", broker=settings.celery.broker, task_cls=EventTask)
