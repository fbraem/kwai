"""Module that defines a period between times."""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta


@dataclass(frozen=True, kw_only=True, slots=True)
class TimePeriod:
    """A period between two times."""

    start: time
    end: time | None = None

    def __post_init__(self):
        """Perform post initialization.

        Raises:
            ValueError: when the start time is before the end time.
        """
        if self.end is not None:
            if self.start > self.end:
                raise ValueError("start should be before end")

    @property
    def endless(self) -> bool:
        """Return True when the period does not have an end time."""
        return self.end is None

    @property
    def delta(self) -> timedelta | None:
        """Return the delta between end and start time.

        Returns: The delta between the start and end time.

        When there is no end time, the result will be None.
        """
        if self.end is None:
            return None

        return datetime.combine(date(1, 1, 1), self.end) - datetime.combine(
            date(1, 1, 1), self.start
        )
