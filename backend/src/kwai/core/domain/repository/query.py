"""Module that defines an interface for a query."""

from abc import abstractmethod
from typing import Any, AsyncIterator


class Query:
    """Interface for a query."""

    @abstractmethod
    async def count(self) -> int:
        """Get the numbers of rows to be returned."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_one(self) -> dict[str, Any] | None:
        """Fetch just one row."""
        raise NotImplementedError

    @abstractmethod
    def fetch(
        self, limit: int | None = None, offset: int | None = None
    ) -> AsyncIterator[dict[str, Any]]:
        """Fetch all rows.

        A generator should be returned to avoid reading all rows at once.
        """
        raise NotImplementedError
