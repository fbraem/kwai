"""Module for defining common classes, functions, ... for use cases."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, NamedTuple


class UseCaseResult(ABC):
    """Base class for a use case result."""

    @abstractmethod
    def to_message(self) -> str:
        """Return a message from the result."""
        raise NotImplementedError


@dataclass(kw_only=True, frozen=True, slots=True)
class NotFoundResult[T](UseCaseResult):
    """A result that indicates that an entity was not found."""

    entity_name: str
    key: T

    def to_message(self) -> str:
        return f"{self.entity_name} with key '{self.key}' not found."


@dataclass(kw_only=True, frozen=True, slots=True)
class EntitiesResult[T](UseCaseResult):
    """A result that returns an iterator for entities and the number of entities."""

    count: int
    entities: AsyncIterator[T]

    def to_message(self) -> str:
        return f"{self.count} entities."


@dataclass(kw_only=True, frozen=True, slots=True)
class EntityResult[T](UseCaseResult):
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
