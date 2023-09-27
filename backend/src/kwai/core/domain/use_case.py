"""Module for defining common classes, functions, ... for use cases."""
from dataclasses import dataclass
from typing import AsyncIterator, NamedTuple


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
