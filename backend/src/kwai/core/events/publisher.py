"""Module for defining an interface for a publisher.

A publisher should publish events to an event bus.
"""

from abc import abstractmethod

from kwai.core.events.event import Event


class Publisher:
    """Interface for a publisher."""

    @abstractmethod
    async def publish(self, event: Event):
        """Publish an event."""
