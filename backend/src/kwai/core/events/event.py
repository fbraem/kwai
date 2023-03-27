"""Module that defines the base class Event."""
import dataclasses
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar


@dataclass(kw_only=True, frozen=True)
class EventMeta:
    """Metadata for the event."""

    name: str


@dataclass(kw_only=True, frozen=True)
class Event:
    """Base class for all events."""

    meta: ClassVar[EventMeta]

    @property
    def data(self) -> dict:
        """Returns a dict that can be used to serialize the event."""
        return {
            "meta": {
                **dataclasses.asdict(self.__class__.meta),
                "date": datetime.utcnow().isoformat(sep=" ", timespec="milliseconds"),
            },
            "data": {**dataclasses.asdict(self)},
        }
