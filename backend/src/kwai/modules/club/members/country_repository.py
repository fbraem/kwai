"""Module that defines an interface for the country repository."""

from abc import ABC, abstractmethod

from kwai.modules.club.members.value_objects import Country


class CountryNotFoundException(Exception):
    """Raised when the country is not found."""


class CountryRepository(ABC):
    """An interface for a country repository."""

    @abstractmethod
    async def get_by_iso_2(self, iso_2: str) -> Country | None:
        """Get a country using the iso2 code of the country."""
