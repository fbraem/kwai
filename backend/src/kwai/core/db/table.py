"""Module for the table decorator."""

from dataclasses import fields, is_dataclass
from typing import Any, Callable, Generic, TypeVar

from sql_smith.functions import alias
from sql_smith.functions import field as sql_field

T = TypeVar("T", bound=Callable)


class Table(Generic[T]):
    """Represent a table in the database.

    With this class a table row can be transformed into a dataclass. It can also
    be used to generate columns or aliases for queries.
    """

    def __init__(self, table_name: str, data_class: T):
        assert is_dataclass(data_class)
        self._table_name: str = table_name
        self._data_class: T = data_class

    @property
    def table_name(self) -> str:
        """Return the table name."""
        return self._table_name

    def __call__(self, row: dict[str, Any]):
        """Shortcut for map_row."""
        return self.map_row(row)

    def alias_name(self, column_name: str, table_name: str | None = None):
        """Return an alias for a column.

        The alias will be the name of the table delimited with an
        underscore: <table_name>_<column_name>.
        By default, the table name associated with the Table instance will be used.

        Args:
            column_name: The name of the column
            table_name: To differ from the current table name, use this table name.

        Returns:
            The alias for the given column.
        """
        table_name = table_name or self._table_name
        return table_name + "_" + column_name

    def aliases(self, table_name: str | None = None):
        """Return aliases for all fields of the dataclass."""
        table_name = table_name or self._table_name
        return [
            alias(table_name + "." + prop.name, self.alias_name(prop.name, table_name))
            for prop in fields(self._data_class)
        ]

    def column(self, column_name: str) -> str:
        """Return column as <table>.<column>."""
        return self._table_name + "." + column_name

    def field(self, column_name: str):
        """Call sql-smith field with the given column.

        short-cut for: field(table.table_name + '.' + column_name)
        """
        return sql_field(self.column(column_name))

    def map_row(self, row: dict[str, Any], table_name: str | None = None) -> T:
        """Map the data of a row to the dataclass.

        Only the fields that have the alias prefix for this table will be selected.
        This makes it possible to pass it a row that contains data from multiple
        tables (which can be the case with a join).
        """
        table_name = table_name or self._table_name
        table_alias = table_name + "_"
        # First, only select the values that belong to this table.
        filtered = {
            k.removeprefix(table_alias): v
            for (k, v) in row.items()
            if k.startswith(table_alias)
        }
        return self._data_class(**filtered)
