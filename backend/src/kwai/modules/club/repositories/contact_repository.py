"""Module that defines an interface for a contact repository."""

from abc import ABC, abstractmethod

from kwai.modules.club.domain.contact import ContactEntity, ContactIdentifier


class ContactNotFoundException(Exception):
    """Raised when the contact cannot be found."""


class ContactRepository(ABC):
    """Interface for a contact repository."""

    @abstractmethod
    async def create(self, contact: ContactEntity) -> ContactEntity:
        """Save a contact entity."""

    @abstractmethod
    async def delete(self, contact: ContactEntity):
        """Delete a contact entity."""

    @abstractmethod
    async def update(self, contact: ContactEntity):
        """Update a contact entity."""

    @abstractmethod
    async def get(self, id_: ContactIdentifier) -> ContactEntity:
        """Get the contact for the given id."""
