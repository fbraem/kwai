"""Module for database classes/functions."""
import dataclasses
from typing import Any, Iterator

import mysql.connector as db
from loguru import logger
from sql_smith import QueryFactory
from sql_smith.engine import MysqlEngine
from sql_smith.functions import field
from sql_smith.query import AbstractQuery, SelectQuery

from kwai.core.db.exceptions import DatabaseException, QueryException
from kwai.core.settings import DatabaseSettings


class Database:
    """Class for communicating with a database.

    When the instance is destroyed and there is a connection, the connection will be
    closed automatically.

    Attributes:
        _connection: The connection handle
        _settings (DatabaseSettings): The settings for this database connection.
    """

    def __init__(self, settings: DatabaseSettings):
        self._connection = None
        self._settings = settings

    def __del__(self):
        """Destructor.

        Closes the connection.
        """
        if self._connection:
            self._connection.close()

    def connect(self):
        """Connect to the database.

        Raises:
            (DatabaseException): Raised when the connection fails.
        """
        try:
            self._connection = db.connect(
                host=self._settings.host,
                database=self._settings.name,
                user=self._settings.user,
                password=self._settings.password,
            )
        except Exception as exc:
            raise DatabaseException(
                f"Connecting to {self._settings.name} failed."
            ) from exc

    @classmethod
    def create_query_factory(cls) -> QueryFactory:
        """Return a query factory for the current database engine.

        The query factory is used to start creating a SELECT, INSERT, UPDATE or
        DELETE query.

        Returns:
            (QueryFactory): The query factory from sql-smith.
                Currently, it returns a query factory for the mysql engine. In the future
                it can provide other engines.
        """
        return QueryFactory(MysqlEngine())

    def commit(self):
        """Commit all changes."""
        self._connection.commit()

    def execute(self, query: AbstractQuery) -> int | None:
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

        with self._connection.cursor() as cursor:
            try:
                cursor.execute(compiled_query.sql, compiled_query.params)
                return cursor.lastrowid
            except Exception as exc:
                raise QueryException(compiled_query.sql) from exc

    def fetch_one(self, query: SelectQuery) -> dict[str, Any] | None:
        """Execute a query and return the first row.

        Args:
            query (SelectQuery): The query to execute.

        Returns:
            (dict[str, Any]): A row is a dictionary using the column names
                as key and the column values as value.
            (None): The query resulted in no rows found.

        Raises:
            (QueryException): Raised when the query contains an error.
        """
        compiled_query = query.compile()
        self.log_query(compiled_query.sql)

        try:
            with self._connection.cursor() as cursor:
                cursor.execute(compiled_query.sql, compiled_query.params)
                column_names = [column[0] for column in cursor.description]
                for row in cursor:
                    # To avoid "unread result found" when not fetching all rows
                    cursor.reset()
                    return {
                        column_name: column
                        for column, column_name in zip(row, column_names, strict=True)
                    }
        except Exception as exc:
            raise QueryException(compiled_query.sql) from exc

        return None  # Nothing found

    def fetch(self, query: SelectQuery) -> Iterator[dict[str, Any]]:
        """Execute a query and yields each row.

        Args:
            query (SelectQuery): The query to execute.

        Yields:
            (dict[str, Any]): A row is a dictionary using the column names
                as key and the column values as value.

        Raises:
            (QueryException): Raised when the query contains an error.
        """
        compiled_query = query.compile()
        self.log_query(compiled_query.sql)

        try:
            with self._connection.cursor() as cursor:
                cursor.execute(compiled_query.sql, compiled_query.params)
                column_names = [column[0] for column in cursor.description]
                for row in cursor:
                    yield {
                        column_name: column
                        for column, column_name in zip(row, column_names, strict=True)
                    }
                # To avoid "unread result found" when not fetching all rows
                cursor.reset()
        except Exception as exc:
            raise QueryException(compiled_query.sql) from exc

    def insert(self, table_name: str, table_data: Any) -> int:
        """Insert a dataclass into the given table.

        Args:
            table_name (str): The name of the table
            table_data (Any): A dataclass containing the values

        Returns:
            (int): The last inserted id

        Raises:
            (QueryException): Raised when the query contains an error.
        """
        assert dataclasses.is_dataclass(table_data), "table_data should be a dataclass"

        record = dataclasses.asdict(table_data)
        del record["id"]
        query = (
            self.create_query_factory()
            .insert(table_name)
            .columns(*record.keys())
            .values(*record.values())
        )
        last_insert_id = self.execute(query)
        return last_insert_id

    def update(self, id_: Any, table_name: str, table_data: Any):
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
        self.execute(query)

    def delete(self, id_: Any, table_name: str):
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
        self.execute(query)

    def log_query(self, query: str):
        """Log a query.

        Args:
            query (str): The query to log.
        """
        db_logger = logger.bind(database=self._settings.name)
        db_logger.info(
            "DB: {database} - Query: {query}", database=self._settings.name, query=query
        )
