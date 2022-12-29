"""Module for the table decorator."""

from dataclasses import fields, is_dataclass
from typing import Any

from sql_smith.functions import alias, field as sql_field


def table(name: str):
    """A decorator that will add some methods to a dataclass for working with database tables.

    The table name will be stored in the __table_name__ class variable.
    """

    def decorator(cls):
        if not is_dataclass(cls):
            raise RuntimeError("The table decorator expects a dataclass")

        def aliases(table_name=name):
            """Returns aliases for all fields of the dataclass."""
            return [
                alias(table_name + "." + prop.name, table_name + "_" + prop.name)
                for prop in fields(cls)
            ]

        def column(column_name: str) -> str:
            return name + "." + column_name

        def field(column_name: str):
            return sql_field(column(column_name))

        def map_row(row: dict[str, Any], table_name=name) -> cls:
            """Maps the data of a row to the dataclass."""
            table_alias = table_name + "_"
            # First, only select the values that belong to this table.
            filtered = {
                k.removeprefix(table_alias): v
                for (k, v) in row.items()
                if k.startswith(table_alias)
            }
            return cls(**filtered)

        cls.aliases = aliases
        cls.column = column
        cls.field = field
        cls.map_row = map_row
        cls.__table_name__ = name
        return cls

    return decorator
