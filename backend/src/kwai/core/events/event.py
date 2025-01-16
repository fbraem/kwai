"""Module that defines the base class Event."""

import dataclasses

from dataclasses import dataclass
from typing import ClassVar

from kwai.core.domain.value_objects.timestamp import Timestamp


@dataclass(kw_only=True, frozen=True)
class EventMeta:
    """Metadata for the event.

    The combination of version, module and name should result in a unique
    full name in kwai and will be used as name for a Redis stream.

    Attributes:
        version: The version of the event.
        module: The module that the event belongs to (e.g. identity)
        name: The name of the event.
    """

    version: str = "v1"
    module: str
    name: str

    @property
    def full_name(self) -> str:
        """Return the full name of the event."""
        return f"kwai/{self.version}/{self.module}/{self.name}"


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
