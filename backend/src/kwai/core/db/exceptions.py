"""Module that defines all database related exceptions."""


class DatabaseException(Exception):
    """Raised when a database error occurred."""

    def __init__(self, msg: str):
        super().__init__(msg)


class QueryException(DatabaseException):
    """Raised when the execution of a query failed."""

    def __init__(self, sql: str):
        super().__init__(sql)
        self._sql = sql

    @property
    def sql(self) -> str:
        """Return the sql statement of the query."""
        return self._sql
