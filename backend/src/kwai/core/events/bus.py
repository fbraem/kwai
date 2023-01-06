"""Module that defines the interface for a bus."""
from abc import abstractmethod
from typing import Any

from kwai.core.domain import Event


class Bus:
    """Interface for a message bus."""

    @abstractmethod
    def publish_event(self, topic: str, event: Event):
        """Publish an event on the given topic."""
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, topic: str, task: Any):
        """Subscribe on a topic."""
        raise NotImplementedError
