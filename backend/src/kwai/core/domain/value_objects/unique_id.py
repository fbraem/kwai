"""Module that defines a value object for a unique id."""

import uuid

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UniqueId:
    """A value object for a unique id."""

    id: uuid.UUID

    @classmethod
    def generate(cls):
        """Create a new unique id (UUID4)."""
        return UniqueId(id=uuid.uuid4())

    @classmethod
    def create_from_string(cls, uuid_str: str):
        """Create a unique id from te string."""
        return UniqueId(id=uuid.UUID(uuid_str))

    def __eq__(self, other):
        """Check if a unique id equals the given id."""
        return str(self) == str(other)

    def __str__(self):
        """Return a string representation."""
        return str(self.id)

    def __hash__(self):
        """Return a hash value for the unique id."""
        return hash(self.id)
