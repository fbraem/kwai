"""Module that defines a value object for a local timestamp."""
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class LocalTimestamp:
    """A value object for a timestamp with a timezone.

    Remark: the datetime should always be in UTC.
    """

    timestamp: datetime
    timezone: str

    @classmethod
    def create_future(cls, **kwargs):
        """Creates a local timestamp in the future.

        The timezone will be UTC.
        """
        return LocalTimestamp(
            timestamp=datetime.now() + timedelta(**kwargs), timezone="UTC"
        )
