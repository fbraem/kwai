"""Module for defining common classes, functions, ... for use cases."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, Generic, NamedTuple, TypeVar


class UseCaseResult(ABC):
    """Base class for a use case result."""

    @abstractmethod
    def to_message(self) -> str:
        """Return a message from the result."""
        raise NotImplementedError


T = TypeVar("T")


@dataclass(kw_only=True, frozen=True, slots=True)
class NotFoundResult(UseCaseResult, Generic[T]):
    """A result that indicates that an entity was not found."""

    entity_name: str
    key: T

    def to_message(self) -> str:
        return f"{self.entity_name} with key '{self.key}' not found."


@dataclass(kw_only=True, frozen=True, slots=True)
class EntitiesResult(UseCaseResult, Generic[T]):
    """A result that returns an iterator for entities and the number of entities."""

    count: int
    entities: AsyncIterator[T]

    def to_message(self) -> str:
        return f"{self.count} entities."


@dataclass(kw_only=True, frozen=True, slots=True)
class EntityResult(UseCaseResult, Generic[T]):
    """A result that returns an entity."""

    entity: T

    def to_message(self) -> str:
        return str(self.entity)


class UseCaseBrowseResult(NamedTuple):
    """A named tuple for a use case that returns a result of browsing entities."""

    count: int
    iterator: AsyncIterator


@dataclass(kw_only=True, frozen=True, slots=True)
class TextCommand:
    """Input for a text."""

    locale: str
    format: str
    title: str
    summary: str
    content: str
