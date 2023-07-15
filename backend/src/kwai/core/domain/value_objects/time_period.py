"""Module that defines a period between times."""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


@dataclass(frozen=True, kw_only=True, slots=True)
class TimePeriod:
    """A period between two times."""

    start: time
    end: time

    def __post_init__(self):
        """Perform post initialization.

        Raises:
            ValueError: when the start time is before the end time.
        """
        if self.start > self.end:
            raise ValueError("start should be before end")

    @property
    def delta(self) -> timedelta:
        """Returns the delta between end and start time."""
        return datetime.combine(date(1, 1, 1), self.end) - datetime.combine(
            date(1, 1, 1), self.start
        )
