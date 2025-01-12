"""Module that defines the base class Event."""

import dataclasses
from dataclasses import dataclass
from typing import ClassVar

from kwai.core.domain.value_objects.timestamp import Timestamp


@dataclass(kw_only=True, frozen=True)
class EventMeta:
    """Metadata for the event."""

    version: str = "v1"
    module: str
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
                "date": str(Timestamp.create_now()),
            },
            "data": {**dataclasses.asdict(self)},
        }
