"""Module that defines the interface for a bus."""
from abc import abstractmethod
from typing import Any

from kwai.core.events.event import Event


class Bus:
    """Interface for a message bus."""

    @abstractmethod
    async def publish(self, event: Event):
        """Publish an event."""
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, event: type[Event], task: Any):
        """Subscribe on an event."""
        raise NotImplementedError
