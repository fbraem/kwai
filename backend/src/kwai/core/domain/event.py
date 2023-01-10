"""Module that defines the base class Event."""
from dataclasses import dataclass
from typing import ClassVar


@dataclass(kw_only=True, frozen=True)
class Event:
    """Base class for all events."""

    name: ClassVar[str]
