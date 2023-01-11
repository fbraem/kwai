"""Module that defines all user recovery events."""
from dataclasses import dataclass
from typing import ClassVar

from kwai.core.domain import EventMeta, Event


@dataclass(kw_only=True, frozen=True)
class UserRecoveryCreatedEvent(Event):
    """Event that is raised when a user recovery is created."""

    meta: ClassVar[EventMeta] = EventMeta(name="identity.user_recovery.created")
    uuid: str
