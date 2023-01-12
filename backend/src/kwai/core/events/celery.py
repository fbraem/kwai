"""Module that configures Celery."""
from abc import ABC

from celery import Celery, Task
from kombu import Queue, Exchange
from loguru import logger

from kwai.core.settings import CelerySettings


class EventTask(Task, ABC):
    """Base class for a task that handles an event."""

    def __call__(self, *args, **kwargs):
        with logger.contextualize(task_id=self.request.id, task_name=self.request.task):
            logger.info("start")
            try:
                result = self.run(*args, **kwargs)
                logger.info("ended")
            except Exception as exc:
                logger.error(f"failed: {exc}")
                raise
        return result


_QUEUES = ("kwai", "identity")


def get_celery_app(settings: CelerySettings):
    """Returns a Celery instance."""
    celery = Celery("kwai", broker=settings.broker, task_cls=EventTask)
    celery.conf.task_create_missing_queues = False
    celery.conf.task_queues = (
        Queue(name=q, exchange=Exchange("q"), routing_key=q) for q in _QUEUES
    )
    celery.conf.task_default_queue = "kwai"
    celery.conf.task_routes = {
        "identity.*": {"queue": "identity"},
    }

    return celery
