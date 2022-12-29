"""Module for database classes/functions."""
import logging
from typing import Any, Generator, Iterator

import mysql.connector as db
from fastapi import Depends
from loguru import logger
from sql_smith import QueryFactory
from sql_smith.engine import MysqlEngine
from sql_smith.query import AbstractQuery

from kwai.core.db.exceptions import DatabaseException, QueryException
from kwai.core.settings import get_settings, Settings, DatabaseSettings


def get_database(settings: Settings = Depends(get_settings)) -> Generator:
    """Dependency that returns a connected database."""
    database = Database(settings.db)
    database.connect()
    yield database


class Database:
    """Wrapper for a database connection."""

    def __init__(self, settings: DatabaseSettings):
        self._connection = None
        self._settings = settings

    def __del__(self):
        if self._connection:
            self._connection.close()

    def connect(self):
        """Connects to the database."""
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
        """Returns a query factory for the current database engine."""
        return QueryFactory(MysqlEngine())

    def commit(self):
        """Commit all changes."""
        self._connection.commit()

    def execute(self, query: AbstractQuery) -> int | None:
        """Executes a query.

        The last rowid from the cursor is returned when the query executed
        successfully. On insert, this can be used to determine the new id of a row.
        """
        compiled_query = query.compile()
        self.log_query(compiled_query.sql)

        with self._connection.cursor() as cursor:
            try:
                cursor.execute(compiled_query.sql, compiled_query.params)
                return cursor.lastrowid
            except Exception as exc:
                raise QueryException(compiled_query.sql) from exc

    def fetch_one(self, query: AbstractQuery) -> dict[str, Any] | None:
        """Executes a query and returns the first row.

        A row is a dictionary build from the column names retrieved from the cursor.
        """
        compiled_query = query.compile()
        self.log_query(compiled_query.sql)

        try:
            with self._connection.cursor() as cursor:
                cursor.execute(compiled_query.sql, compiled_query.params)
                column_names = [column[0] for column in cursor.description]
                for row in cursor:
                    cursor.reset()  # To avoid "unread result found" when not fetching all rows
                    return {
                        column_name: column
                        for column, column_name in zip(row, column_names)
                    }
        except Exception as exc:
            raise QueryException(compiled_query.sql) from exc

        return None  # Nothing found

    def fetch(self, query: AbstractQuery) -> Iterator[dict[str, Any]]:
        """Executes a query and yields each row.

        A row is a dictionary build from the column names retrieved from the cursor.
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
                        for column, column_name in zip(row, column_names)
                    }
                cursor.reset()  # To avoid "unread result found" when not fetching all rows
        except Exception as exc:
            raise QueryException(compiled_query.sql) from exc

    def log_query(self, query: str):
        db_logger = logger.bind(database=self._settings.name)
        db_logger.info(
            "DB: {database} - Query: {query}", database=self._settings.name, query=query
        )
