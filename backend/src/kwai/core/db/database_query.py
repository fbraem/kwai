"""Module that implements a query for a database."""
from abc import abstractmethod
from typing import Iterator

from sql_smith.functions import alias, func
from sql_smith.query import SelectQuery

from kwai.core.db import Database
from kwai.core.domain.repository.query import Query


class DatabaseQuery(Query):
    """Creates a query using a database."""

    def __init__(self, database: Database):
        self._database: Database = database
        self._query: SelectQuery = Database.create_query_factory().select()
        self.init()

    @abstractmethod
    def init(self):
        """Override this method to create the base query."""
        pass

    @property
    @abstractmethod
    def columns(self):
        """Returns the columns used in the query."""
        pass

    @property
    def count_column(self) -> str:
        """The column used to count records."""
        return "id"

    def count(self) -> int:
        """Executes the query and uses the count_column to count the number of records."""

        # Reset limit/offset to avoid a wrong result
        self._query.limit(None)
        self._query.offset(None)

        self._query.columns(
            alias(func("COUNT", func("DISTINCT", self.count_column)), "c")
        )
        result = self._database.fetch_one(self._query)
        return int(result["c"])

    def fetch_one(self):
        self._query.columns(*self.columns)
        return self._database.fetch_one(self._query)

    def fetch(
        self, limit: int | None = None, offset: int | None = None
    ) -> Iterator[dict[str, any]]:
        self._query.limit(limit)
        self._query.offset(offset)
        self._query.columns(*self.columns)

        return self._database.fetch(self._query)
