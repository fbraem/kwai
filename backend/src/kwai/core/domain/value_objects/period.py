"""Module that defines the value object Period."""

from dataclasses import dataclass, field
from datetime import timedelta

from kwai.core.domain.value_objects.timestamp import Timestamp


@dataclass(frozen=True, kw_only=True, slots=True)
class Period:
    """Value object for handling a period between dates."""

    start_date: Timestamp = field(default_factory=Timestamp.create_now)
    end_date: Timestamp = field(default_factory=Timestamp)

    def __post_init__(self):
        """Perform post initialization.

        Raises:
            ValueError: when the start date is before the end date.
        """
        if not self.end_date.empty:
            if self.start_date.timestamp > self.end_date.timestamp:
                raise ValueError("start_date should be before end_date")

    @property
    def delta(self) -> timedelta | None:
        """Return the delta between end and start time."""
        if not self.end_date.empty:
            return self.end_date.timestamp - self.start_date.timestamp
        return None

    @property
    def endless(self) -> bool:
        """Return True when end date is not set."""
        return self.end_date.empty

    @classmethod
    def create_from_delta(cls, start_date: Timestamp = None, **kwargs) -> "Period":
        """Create a period from a delta."""
        date = start_date or Timestamp.create_now()
        return Period(start_date=date, end_date=date.add_delta(**kwargs))
