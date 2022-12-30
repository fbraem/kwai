"""Module that defines a value object for a local timestamp."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LocalTimestamp:
    """A value object for a timestamp with a timezone.

    Remark: the datetime should always be in UTC.
    """

    timestamp: datetime
    timezone: str
