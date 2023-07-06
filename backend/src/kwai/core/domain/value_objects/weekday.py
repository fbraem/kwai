"""Module for defining a value object for a weekday."""

from datetime import datetime
from enum import Enum


class Weekday(Enum):
    """Represent a day in the week."""

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @classmethod
    def create_from_date(cls, date: datetime):
        """Create a Weekday from a date.

        Args:
            date: The date to extract the weekday from.
        """
        return Weekday(date.weekday() + 1)
