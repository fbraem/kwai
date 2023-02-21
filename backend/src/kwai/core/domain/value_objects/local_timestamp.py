"""Module that defines a value object for a local timestamp."""
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class LocalTimestamp:
    """A value object for a timestamp with a timezone.

    The datetime should always be in UTC. The timezone can be used by the frontend
    to convert the time to the original timezone.
    """

    timestamp: datetime = None
    timezone: str = "UTC"

    @property
    def empty(self):
        """Is the timestamp known?"""
        return self.timestamp is None

    @property
    def is_past(self) -> bool:
        """Is the timestamp in the past?"""
        assert not self.empty, "No datetime set"

        return self.timestamp < datetime.utcnow()

    @classmethod
    def create_with_delta(cls, **kwargs):
        """Create a current local timestamp and applies the delta.

        The timezone will be UTC.
        """
        return LocalTimestamp(timestamp=datetime.utcnow() + timedelta(**kwargs))

    @classmethod
    def create_now(cls):
        """Create a timestamp with the current UTC time."""
        return LocalTimestamp(timestamp=datetime.utcnow())
