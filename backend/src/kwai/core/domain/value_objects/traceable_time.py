"""Module that defines a value object to trace creation/update time of an entity."""

from dataclasses import dataclass, field

from kwai.core.domain.value_objects.timestamp import Timestamp


@dataclass(frozen=True, kw_only=True)
class TraceableTime:
    """A value object to track creation/update time."""

    created_at: Timestamp = field(default_factory=Timestamp.create_now)
    updated_at: Timestamp = field(default_factory=Timestamp)

    @property
    def is_updated(self):
        """Check if this entity has been updated."""
        return not self.updated_at.empty()

    def mark_for_update(self) -> "TraceableTime":
        """Set the update time to the current time."""
        return TraceableTime(
            created_at=self.created_at, updated_at=Timestamp.create_now()
        )
