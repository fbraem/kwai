"""Module that defines a value object for a unique id."""
import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UniqueId:
    """A value object for a unique id."""

    id: uuid.UUID  # pylint: disable=C0103

    @classmethod
    def generate(cls):
        """Creates a new unique id (UUID4)."""
        return UniqueId(id=uuid.uuid4())

    @classmethod
    def create_from_string(cls, s: str):
        return UniqueId(id=uuid.UUID(s))

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return str(self.id)
