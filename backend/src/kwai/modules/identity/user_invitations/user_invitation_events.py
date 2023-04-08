"""Module that defines all user invitation events."""
from dataclasses import dataclass
from typing import ClassVar

from kwai.core.events.event import Event, EventMeta


@dataclass(kw_only=True, frozen=True, slots=True)
class UserInvitationCreatedEvent(Event):
    """Event raised when a user invitation is created."""

    meta: ClassVar[EventMeta] = EventMeta(name="identity.user_invitation.created")
    uuid: str
