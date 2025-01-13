"""Module for database classes/functions."""

import dataclasses

from typing import Any, AsyncIterator, TypeAlias

import asyncmy

from loguru import logger
from sql_smith import QueryFactory
from sql_smith.engine import MysqlEngine
from sql_smith.functions import field
from sql_smith.query import AbstractQuery, SelectQuery

from kwai.core.db.exceptions import DatabaseException, QueryException
from kwai.core.settings import DatabaseSettings


Record: TypeAlias = dict[str, Any]


class Database:
    """Class for communicating with a database.

    Attributes:
        _connection: A connection
        _settings (DatabaseSettings): The settings for this database connection.
    """

    def __init__(self, settings: DatabaseSettings):
        self._connection: asyncmy.Connection | None = None
        self._settings = settings

    async def setup(self):
        """Set up the connection pool."""
        try:
            self._connection = await asyncmy.connect(
                host=self._settings.host,
                database=self._settings.name,
                user=self._settings.user,
                password=self._settings.password,
            )
        except Exception as exc:
            raise DatabaseException(
                f"Setting up connection for database {self._settings.name} "
                f"failed: {exc}"
            ) from exc

    async def check_connection(self):
        """Check if the connection is set, if not it will try to connect."""
        if self._connection is None:
            await self.setup()

    async def close(self):
        """Close the connection."""
        if self._connection:
            await self._connection.ensure_closed()
            self._connection = None

    @classmethod
    def create_query_factory(cls) -> QueryFactory:
        """Return a query factory for the current database engine.

        The query factory is used to start creating a SELECT, INSERT, UPDATE or
        DELETE query.

        Returns:
            (QueryFactory): The query factory from sql-smith.
                Currently, it returns a query factory for the mysql engine. In the
                future it can provide other engines.
        """
        return QueryFactory(MysqlEngine())

    async def commit(self):
        """Commit all changes."""
        await self.check_connection()
        await self._connection.commit()

    async def execute(self, query: AbstractQuery) -> int | None:
        """Execute a query.

        The last rowid from the cursor is returned when the query executed
        successfully. On insert, this can be used to determine the new id of a row.

        Args:
            query (AbstractQuery): The query to execute.

        Returns:
            (int): When the query is an insert query, it will return the last rowid.
            (None): When there is no last rowid.

        Raises:
            (QueryException): Raised when the query contains an error.
        """
        compiled_query = query.compile()
        self.log_query(compiled_query.sql)

        await self.check_connection()
        async with self._connection.cursor() as cursor:
            try:
                await cursor.execute(compiled_query.sql, compiled_query.params)
                if cursor.rowcount != -1:
                    self.log_affected_rows(cursor.rowcount)
                return cursor.lastrowid
            except Exception as exc:
                raise QueryException(compiled_query.sql) from exc

    async def fetch_one(self, query: SelectQuery) -> Record | None:
        """Execute a query and return the first row.

        Args:
            query (SelectQuery): The query to execute.

        Returns:
            (Record): A row is a dictionary using the column names
                as key and the column values as value.
            (None): The query resulted in no rows found.

        Raises:
            (QueryException): Raised when the query contains an error.
        """
        compiled_query = query.compile()
        self.log_query(compiled_query.sql)

        await self.check_connection()
        try:
            async with self._connection.cursor() as cursor:
                await cursor.execute(compiled_query.sql, compiled_query.params)
                column_names = [column[0] for column in cursor.description]
                if row := await cursor.fetchone():
                    return {
                        column_name: column
                        for column, column_name in zip(row, column_names, strict=True)
                    }
        except Exception as exc:
            raise QueryException(compiled_query.sql) from exc

        return None  # Nothing found

    async def fetch(self, query: SelectQuery) -> AsyncIterator[Record]:
        """Execute a query and yields each row.

        Args:
            query (SelectQuery): The query to execute.

        Yields:
            (Record): A row is a dictionary using the column names
                as key and the column values as value.

        Raises:
            (QueryException): Raised when the query contains an error.
        """
        compiled_query = query.compile()
        self.log_query(compiled_query.sql)

        await self.check_connection()
        try:
            async with self._connection.cursor() as cursor:
                await cursor.execute(compiled_query.sql, compiled_query.params)
                column_names = [column[0] for column in cursor.description]
                while row := await cursor.fetchone():
                    yield {
                        column_name: column
                        for column, column_name in zip(row, column_names, strict=True)
                    }
        except Exception as exc:
            raise QueryException(compiled_query.sql) from exc

    async def insert(self, table_name: str, *table_data: Any) -> int:
        """Insert one or more instances of a dataclass into the given table.

        Args:
            table_name (str): The name of the table
            table_data (Any): One or more instances of a dataclass containing the values

        Returns:
            (int): The last inserted id. When multiple inserts are performed, this will
                be the id of the last executed insert.

        Raises:
            (QueryException): Raised when the query contains an error.
        """
        assert dataclasses.is_dataclass(table_data[0]), (
            "table_data should be a dataclass"
        )

        record = dataclasses.asdict(table_data[0])
        if "id" in record:
            del record["id"]
        query = self.create_query_factory().insert(table_name).columns(*record.keys())

        for data in table_data:
            assert dataclasses.is_dataclass(data), "table_data should be a dataclass"
            record = dataclasses.asdict(data)
            if "id" in record:
                del record["id"]
            query = query.values(*record.values())

        last_insert_id = await self.execute(query)
        return last_insert_id

    async def update(self, id_: Any, table_name: str, table_data: Any):
        """Update a dataclass in the given table.

        Args:
            id_ (Any): The id of the data to update.
            table_name: The name of the table.
            table_data: The dataclass containing the data.

        Raises:
            (QueryException): Raised when the query contains an error.
        """
        assert dataclasses.is_dataclass(table_data), "table_data should be a dataclass"

        record = dataclasses.asdict(table_data)
        del record["id"]
        query = (
            self.create_query_factory()
            .update(table_name)
            .set(record)
            .where(field("id").eq(id_))
        )
        await self.execute(query)

    async def delete(self, id_: Any, table_name: str):
        """Delete a row from the table using the id field.

        Args:
            id_ (Any): The id of the row to delete.
            table_name (str): The name of the table.

        Raises:
            (QueryException): Raised when the query results in an error.
        """
        query = (
            self.create_query_factory().delete(table_name).where(field("id").eq(id_))
        )
        await self.execute(query)

    def log_query(self, query: str):
        """Log a query.

        Args:
            query (str): The query to log.
        """
        db_logger = logger.bind(database=self._settings.name)
        db_logger.info(
            "DB: {database} - Query: {query}", database=self._settings.name, query=query
        )

    def log_affected_rows(self, rowcount: int):
        """Log the number of affected rows of the last executed query.

        Args:
            rowcount: The number of affected rows.
        """
        db_logger = logger.bind(database=self._settings.name)
        db_logger.info(
            "DB: {database} - Affected rows: {rowcount}",
            database=self._settings.name,
            rowcount=rowcount,
        )

    @property
    def settings(self) -> DatabaseSettings:
        """Return the database settings.

        This property is immutable: the returned value is a copy of the current
        settings.
        """
        return self._settings.copy()

    async def begin(self):
        """Start a transaction."""
        await self.check_connection()
        await self._connection.begin()

    async def rollback(self):
        """Rollback a transaction."""
        await self.check_connection()
        await self._connection.rollback()
