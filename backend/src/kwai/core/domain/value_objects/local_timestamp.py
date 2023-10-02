"""Module that defines a value object for a local timestamp."""
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


@dataclass(frozen=True)
class LocalTimestamp:
    """A value object for a timestamp.

    The datetime should always be in UTC.
    """

    timestamp: datetime = None

    @property
    def empty(self):
        """Return True when the timestamp is unknown."""
        return self.timestamp is None

    @property
    def is_past(self) -> bool:
        """Return True when the timestamp in the past."""
        assert not self.empty, "No datetime set"

        return self.timestamp < datetime.utcnow()

    @property
    def year(self) -> int:
        """Return the year."""
        if self.timestamp is None:
            raise ValueError("Empty timestamp")
        return self.timestamp.year

    @property
    def month(self) -> int:
        """Return the month."""
        if self.timestamp is None:
            raise ValueError("Empty timestamp")
        return self.timestamp.month

    @property
    def day(self) -> int:
        """Return the day."""
        if self.timestamp is None:
            raise ValueError("Empty timestamp")
        return self.timestamp.day

    @property
    def hours(self) -> int:
        """Return the hours."""
        if self.timestamp is None:
            raise ValueError("Empty timestamp")
        return self.timestamp.hour

    @property
    def minutes(self) -> int:
        """Return the minutes."""
        if self.timestamp is None:
            raise ValueError("Empty timestamp")
        return self.timestamp.minute

    @property
    def seconds(self) -> int:
        """Return the seconds."""
        if self.timestamp is None:
            raise ValueError("Empty timestamp")
        return self.timestamp.second

    @property
    def date(self) -> date:
        """Return the date."""
        if self.timestamp is None:
            raise ValueError("Empty timestamp")
        return self.timestamp.date()

    @property
    def time(self) -> time:
        """Return the date."""
        if self.timestamp is None:
            raise ValueError("Empty timestamp")
        return self.timestamp.time()

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
        """Create a current local timestamp and applies the delta."""
        return cls.create_now().add_delta(**kwargs)

    @classmethod
    def create_now(cls):
        """Create a timestamp with the current UTC time."""
        return LocalTimestamp(timestamp=datetime.utcnow())

    @classmethod
    def create_from_string(
        cls, date_time: str | None = None, date_format: str = "%Y-%m-%d %H:%M:%S"
    ) -> "LocalTimestamp":
        """Create a timestamp from a string.

        Args:
            date_time: The string to convert to a timestamp.
            date_format: The format used in the string.
        """
        if date_time is None:
            return LocalTimestamp()
        return LocalTimestamp(datetime.strptime(date_time, date_format))
