"""Module that defines identifiers."""

from abc import ABC, abstractmethod

from kwai.core.domain.value_objects.unique_id import UniqueId


class Identifier[T](ABC):
    """Abstract and generic class for an identifier."""

    def __init__(self, id_: T):
        self._id = id_

    @property
    def value(self) -> T:
        """Return the id."""
        return self._id

    def __eq__(self, other: object):
        """Check the equality of identifiers."""
        if isinstance(other, Identifier):
            return self._id == other._id
        return False

    def __hash__(self):
        """Create a hash for an identifier."""
        return hash(self._id)

    @abstractmethod
    def is_empty(self) -> bool:
        """Return true when the identifier is not set."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Return the string representation of the id."""
        return str(self._id)


class IntIdentifier(Identifier[int]):
    """Class that implements an identifier with an integer."""

    def __init__(self, id_: int = 0):
        super().__init__(id_)

    def is_empty(self) -> bool:
        """Return True when the id equals 0."""
        return self.value == 0

    def __repr__(self):
        """Return a string representation of the identifier."""
        return f"IntIdentifier={self.value}"


class UniqueIdIdentifier(Identifier[UniqueId]):
    """Class that implements an identifier with a UniqueId."""

    def __init__(self, id_: UniqueId | None = None):
        super().__init__(id_ or UniqueId.generate())

    def is_empty(self) -> bool:
        """This identifier type is never empty."""
        return False

    def __repr__(self):
        """Return a string representation of the identifier."""
        return f"UniqueIdIdentifier={self.value}"
