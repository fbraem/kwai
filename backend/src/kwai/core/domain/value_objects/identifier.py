"""Module that defines identifiers."""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class Identifier(ABC, Generic[T]):
    """Abstract and generic class for an identifier."""

    def __init__(self, id_: T):
        self._id = id_

    @property
    def value(self) -> T:
        return self._id

    @abstractmethod
    def is_empty(self) -> bool:
        """Returns true when the identifier is not set."""
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self._id)


class IntIdentifier(Identifier[int]):
    """Class that implements an identifier with an integer."""

    def __init__(self, id_: int = 0):
        super().__init__(id_)

    def is_empty(self) -> bool:
        return self.value == 0
