from dataclasses import dataclass, field

from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp


@dataclass(frozen=True, kw_only=True, slots=True)
class Period:
    """Value object for handling a period between dates."""

    start_date: LocalTimestamp = field(default_factory=LocalTimestamp.create_now)
    end_date: LocalTimestamp = field(default_factory=LocalTimestamp)
