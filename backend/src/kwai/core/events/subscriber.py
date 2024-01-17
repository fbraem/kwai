"""Module for defining an interface for a subscriber."""
from abc import ABC, abstractmethod
from typing import Any, Callable

from kwai.core.events.event import Event


class Subscriber(ABC):
    """Interface for a subscriber."""

    @abstractmethod
    def subscribe(
        self, event: type[Event], task: Callable[[dict[str, Any]], Any]
    ) -> None:
        """Subscribe to an event with the given task.

        It must be possible to attach multiple tasks to the same event.
        """
