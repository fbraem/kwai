"""Module that implements a message bus with Celery."""
from typing import Any

from kwai.core.domain import Event
from kwai.core.events import Bus


class CeleryBus(Bus):
    """Message bus using Celery."""

    def subscribe(self, topic: str, task: Any):
        pass

    def publish_event(self, topic: str, event: Event):
        pass
