"""Module that defines a value object to trace creation/update time of an entity."""
import datetime
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class TraceableTime:
    """A value object to track creation/update time."""

    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime | None = None

    @property
    def is_updated(self):
        """Is this entity updated?"""
        return self.updated_at is not None

    def mark_for_update(self):
        """Set the update time to the current time."""
        self.updated_at = datetime.datetime.utcnow()
