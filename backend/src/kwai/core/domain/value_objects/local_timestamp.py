"""Module that defines a value object for a local timestamp."""
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class LocalTimestamp:
    """A value object for a timestamp with a timezone.

    The datetime should always be in UTC.
    """

    timestamp: datetime = None

    @property
    def empty(self):
        """Return Tru when the timestamp is known."""
        return self.timestamp is None

    @property
    def is_past(self) -> bool:
        """Return True when the timestamp in the past."""
        assert not self.empty, "No datetime set"

        return self.timestamp < datetime.utcnow()

    def __str__(self) -> str:
        """Return a string representation.

        Returns:
            A formatted timestamp in format YYYY-MM-DD HH:mm:ss.
            An empty string will be returned, when no timestamp is available.
        """
        if self.empty:
            return ""

        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def add_delta(self, **kwargs) -> "LocalTimestamp":
        """Create a new timestamp by adding the delta to the timestamp.

        Returns:
            LocalTimestamp: A new timestamp with the delta.
        """
        return LocalTimestamp(self.timestamp + timedelta(**kwargs))

    @classmethod
    def create_with_delta(cls, **kwargs):
        """Create a current local timestamp and applies the delta.

        The timezone will be UTC.
        """
        return cls.create_now().add_delta(**kwargs)

    @classmethod
    def create_now(cls):
        """Create a timestamp with the current UTC time."""
        return LocalTimestamp(timestamp=datetime.utcnow())
