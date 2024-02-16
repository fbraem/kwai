"""Module for defining value objects for the members module."""
from dataclasses import dataclass
from enum import Enum

from kwai.core.domain.value_objects.date import Date


@dataclass(kw_only=True, frozen=True, slots=True)
class License:
    """A license of a member."""

    number: str
    end_date: Date

    @property
    def expired(self):
        """Is this license expired?"""
        return self.end_date.past

    def __str__(self) -> str:
        """Return a string representation of a license."""
        return self.number


class Gender(Enum):
    """The gender of a person."""

    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


@dataclass(kw_only=True, frozen=True, slots=True)
class Birthdate:
    """A birthdate of a person."""

    date: Date

    @property
    def age(self) -> int:
        """Return the age on the current day."""
        return self.date.get_age(self.date.today())

    def get_age_in_year(self, year: int) -> int:
        """Return the age that will be reached in the given year."""
        date = Date.create(year, 12, 31)
        return self.date.get_age(date)

    def __str__(self) -> str:
        """Return a string representation of a birthdate."""
        return str(self.date)


@dataclass(kw_only=True, frozen=True, slots=True)
class Country:
    """A country."""

    id: int
    iso_2: str
    iso_3: str

    def __str__(self) -> str:
        """Returns a string representation (iso_2) of the country."""
        return self.iso_2


@dataclass(kw_only=True, frozen=True, slots=True)
class Address:
    """An address."""

    address: str
    postal_code: str
    city: str
    county: str
    country: Country
