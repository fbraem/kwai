"""Module that defines all database related exceptions."""


class DatabaseException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class QueryException(DatabaseException):
    def __init__(self, sql: str):
        super().__init__(sql)
        self._sql = sql

    @property
    def sql(self) -> str:
        return self._sql
