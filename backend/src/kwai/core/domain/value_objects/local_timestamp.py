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

    @classmethod
    def create_future(cls, **kwargs):
        """Create a local timestamp in the future.

        The timezone will be UTC.
        """
        return LocalTimestamp(timestamp=datetime.utcnow() + timedelta(**kwargs))

    @classmethod
    def create_now(cls):
        """Create a timestamp with the current time."""
        return LocalTimestamp(timestamp=datetime.utcnow())
