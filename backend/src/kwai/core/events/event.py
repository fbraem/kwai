"""Module that defines the base class Event."""
import dataclasses
from dataclasses import dataclass
from typing import ClassVar


@dataclass(kw_only=True, frozen=True)
class EventMeta:
    name: str


@dataclass(kw_only=True, frozen=True)
class Event:
    """Base class for all events."""

    meta: ClassVar[EventMeta]

    @property
    def data(self) -> dict:
        """Returns a dict that can be used to serialize the event."""
        return {
            "meta": {**dataclasses.asdict(self.__class__.meta)},
            "data": {**dataclasses.asdict(self)},
        }
