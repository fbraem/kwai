from dataclasses import dataclass, field
from datetime import timedelta

from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp


@dataclass(frozen=True, kw_only=True, slots=True)
class Period:
    """Value object for handling a period between dates."""

    start_date: LocalTimestamp = field(default_factory=LocalTimestamp.create_now)
    end_date: LocalTimestamp = field(default_factory=LocalTimestamp)

    def __post_init__(self):
        """Perform post initialization.

        Raises:
            ValueError: when the start date is before the end date.
        """
        if self.start_date.timestamp > self.end_date.timestamp:
            raise ValueError("start_date should be before end_date")

    @property
    def delta(self) -> timedelta:
        """Return the delta between end and start time."""
        return self.end_date.timestamp - self.start_date.timestamp
