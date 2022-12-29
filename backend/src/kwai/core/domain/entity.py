"""Module that defines a generic entity."""
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(kw_only=True, frozen=True)
class Entity(Generic[T]):
    """A generic wrapper around a domain object for adding an id."""

    id: int
    domain: T

    def __call__(self, *args, **kwargs) -> T:
        """A shortcut for getting the domain object."""
        return self.domain
