"""Module for the table decorator."""

from dataclasses import fields, is_dataclass
from typing import Any

from sql_smith.functions import alias
from sql_smith.functions import field as sql_field


# noinspection PyPep8Naming
class table:  # pylint: disable=invalid-name, too-few-public-methods
    """A decorator that will add methods to a dataclass for handling database tables.

    The table name will be stored in the __table_name__ class variable.
    """

    def __init__(self, name: str):
        self._table_name = name

    def __call__(self, data_class: Any):
        """Wrapping the dataclass with Table class."""
        assert is_dataclass(data_class)

        class Table(data_class):
            """A class that represents a table record."""

            __table_name__: str = self._table_name

            @classmethod
            def aliases(
                cls, table_name=self._table_name
            ):  # pylint: disable=protected-access
                """Return aliases for all fields of the dataclass."""
                return [
                    alias(table_name + "." + prop.name, table_name + "_" + prop.name)
                    for prop in fields(cls)
                ]

            @classmethod
            def column(cls, column_name: str) -> str:
                """Return column as <table>.<column>."""
                return cls.__table_name__ + "." + column_name

            @classmethod
            def field(cls, column_name: str):
                """Call sql-smith field with the given column.

                short-cut for: field(table.__table__name__ + '.' + column_name)
                """
                return sql_field(cls.column(column_name))

            @classmethod
            def map_row(
                cls,
                row: dict[str, Any],
                table_name=self._table_name,  # pylint: disable=protected-access
            ) -> data_class:
                """Map the data of a row to the dataclass."""
                table_alias = table_name + "_"
                # First, only select the values that belong to this table.
                filtered = {
                    k.removeprefix(table_alias): v
                    for (k, v) in row.items()
                    if k.startswith(table_alias)
                }
                return data_class(**filtered)

        return Table
