"""Module for defining an interface for a subscriber."""
from abc import ABC, abstractmethod

from kwai.core.events.event_router import EventRouter


class Subscriber(ABC):
    """Interface for a subscriber."""

    @abstractmethod
    def subscribe(self, event: EventRouter) -> None:
        """Subscribe to an event with the given task."""
