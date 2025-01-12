"""Module for defining an event router."""

import inspect
from dataclasses import dataclass
from typing import Any, Callable, Type

from loguru import logger

from kwai.core.events.event import Event

EventCallbackType = Callable[[dict[str, Any]], Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class EventRouter:
    """A router that defines which method must be called on an event."""

    event: Type[Event]
    callback: EventCallbackType

    async def execute(self, event_data: dict[str, Any]) -> bool:
        """Executes the callback."""
        try:
            if inspect.iscoroutinefunction(self.callback):
                await self.callback(event_data)
            else:
                self.callback(event_data)
        except Exception as ex:
            logger.warning(f"The handler raised an exception: {ex!r}")
            return False
        return True
