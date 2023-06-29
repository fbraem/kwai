"""Module for defining common classes, functions, ... for use cases."""
from typing import AsyncIterator, NamedTuple


class UseCaseBrowseResult(NamedTuple):
    """A named tuple for a use case that returns a result of browsing entities."""

    count: int
    iterator: AsyncIterator
