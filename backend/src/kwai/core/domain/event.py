"""Module that defines the base class Event."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    """Base class for all events."""
