"""Module that implements a message bus with Celery."""
import celery

from kwai.core.events import Event, Bus


class CeleryBus(Bus):
    """Message bus using Celery.

    Remark:
        Derived from https://github.com/Mulugruntz/celery-pubsub
    """

    def __init__(self, celery_app: celery):
        self._celery_app = celery_app
        self._subscribed = set()
        self._jobs = {}

    def subscribe(self, event: type[Event], task: celery.Task):
        if task.name not in self._celery_app.tasks:
            self._celery_app.register_task(task)
        key = (event.meta.name, task)
        if key not in self._subscribed:
            self._subscribed.add(key)
            self._jobs = {}

    def publish(self, event: Event) -> None:
        self._get_jobs(event).delay(event.data)

    def _get_jobs(self, event: Event):
        """Find all tasks for the given event."""
        if event.meta.name not in self._jobs:
            jobs = []
            for job in self._subscribed:
                if job[0] == event.meta.name:
                    jobs.append(job[1].s())
            self._jobs[event.meta.name] = celery.group(jobs)
        return self._jobs[event.meta.name]
