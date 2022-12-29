"""Module that defines an interface for a query."""
from abc import abstractmethod
from typing import Any, Iterator


class Query:
    """Interface for a query."""

    @abstractmethod
    def count(self) -> int:
        """Get the numbers of rows to be returned."""
        raise NotImplementedError

    @abstractmethod
    def fetch_one(self) -> dict[str, Any]:
        """Fetch just one row."""
        raise NotImplementedError

    @abstractmethod
    def fetch(
        self, limit: int | None = None, offset: int | None = None
    ) -> Iterator[dict[str, Any]]:
        """Fetch all rows. A generator should be returned to avoid reading all rows at once."""
        raise NotImplementedError
