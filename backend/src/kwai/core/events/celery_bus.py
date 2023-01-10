"""Module that implements a message bus with Celery."""
from typing import Any

import celery
from celery import Task

from kwai.core.domain import Event
from kwai.core.events import Bus


class CeleryBus(Bus):
    """Message bus using Celery."""

    def __init__(self):
        self._subscribed = set()
        self._jobs = {}

    def subscribe(self, event: type[Event], task: Task):
        key = (event.name, task)
        if key not in self._subscribed:
            self._subscribed.add(key)
            self._jobs = {}

    def publish(self, event: Event):
        result = self._get_jobs(event).delay(event.__dict__)
        return result

    def _get_jobs(self, event: Event):
        if event.name not in self._jobs:
            jobs = []
            for job in self._subscribed:
                if job[0] == event.name:
                    jobs.append(job[1].s())
            self._jobs[event.name] = celery.group(jobs)
        return self._jobs[event.name]
