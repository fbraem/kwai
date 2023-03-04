"""Module that defines a value object to trace creation/update time of an entity."""
from dataclasses import dataclass, field

from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp


@dataclass(frozen=True, kw_only=True)
class TraceableTime:
    """A value object to track creation/update time."""

    created_at: LocalTimestamp = field(default_factory=LocalTimestamp.create_now)
    updated_at: LocalTimestamp = field(default_factory=LocalTimestamp)

    @property
    def is_updated(self):
        """Is this entity updated?"""
        return not self.updated_at.empty()

    def mark_for_update(self) -> "TraceableTime":
        """Set the update time to the current time."""
        return TraceableTime(
            created_at=self.created_at, updated_at=LocalTimestamp.create_now()
        )
