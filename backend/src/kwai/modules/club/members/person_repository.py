"""Module that defines an interface for a person repository."""

from abc import ABC, abstractmethod

from kwai.modules.club.members.person import PersonEntity, PersonIdentifier


class PersonNotFoundException(Exception):
    """Raised when a person cannot be found."""


class PersonRepository(ABC):
    """An interface for a person repository."""

    @abstractmethod
    async def create(self, person: PersonEntity) -> PersonEntity:
        """Save a person entity."""

    @abstractmethod
    async def update(self, person: PersonEntity) -> None:
        """Update a person entity."""

    @abstractmethod
    async def delete(self, person: PersonEntity):
        """Delete a person entity."""

    @abstractmethod
    async def get(self, id_: PersonIdentifier) -> PersonEntity:
        """Get the person for the given id."""
