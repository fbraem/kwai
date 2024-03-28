"""Module that defines an interface for the country repository."""

from abc import ABC, abstractmethod

from kwai.modules.club.members.country import CountryEntity


class CountryNotFoundException(Exception):
    """Raised when the country is not found."""


class CountryRepository(ABC):
    """An interface for a country repository."""

    @abstractmethod
    async def get_by_iso_2(self, iso_2: str) -> CountryEntity:
        """Get a country using the iso2 code of the country."""

    @abstractmethod
    async def create(self, country: CountryEntity):
        """Save a country in the repository."""

    @abstractmethod
    async def delete(self, country: CountryEntity):
        """Delete a country from the repository."""
