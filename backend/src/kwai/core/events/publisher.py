"""Module for defining an interface for a publisher.

A publisher should publish events to a broker. Subscribers should be defined to
receive and process the event. It must be possible have different subscribes that
handle the same event (pub/sub).
"""
from abc import abstractmethod

from kwai.core.events.event import Event


class Publisher:
    """Interface for a publisher."""

    @abstractmethod
    def publish(self, event: Event):
        """Publish an event."""
