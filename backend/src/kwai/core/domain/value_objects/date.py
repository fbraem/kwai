"""Module for defining a date value object."""
from dataclasses import dataclass

import pendulum


@dataclass(kw_only=True, frozen=True, slots=True)
class Date:
    """An immutable value object for a date.

    This class is a decorator of a pendulum object.
    See: https://pendulum.eustace.io
    """

    date: pendulum

    @property
    def day(self) -> int:
        """Return the day of the date."""
        return self.date.day

    def end_of(self, unit: str) -> "Date":
        """Returns a new date resetting it to the end of the given unit."""
        return Date(date=self.date.end_of(unit))

    def get_age(self, some_date: "Date"):
        """Return the age on the given date."""
        return (
            some_date.year
            - self.date.year
            - ((some_date.month, some_date.day) < (self.date.month, self.date.day))
        )

    @property
    def month(self) -> int:
        """Return the month of the date."""
        return self.date.month

    @property
    def year(self) -> int:
        """Return the year of the date."""
        return self.date.year

    @classmethod
    def today(cls) -> "Date":
        """Return today as date."""
        return Date(date=pendulum.today())

    @classmethod
    def create_from_string(cls, value: str, format_: str = "YYYY-MM-DD") -> "Date":
        """Create a Date from a string."""
        return Date(date=pendulum.from_format(value, format_))

    @classmethod
    def create(cls, year: int, month: int = 1, day: int = 1):
        """Create a date with the given year, month and day."""
        return Date(date=pendulum.date(year, month, day))

    def __str__(self) -> str:
        """Return a string representation of the date."""
        return self.date.to_date_string()
