"""Module that defines some dataclasses that can be used as data transfer objects."""

from dataclasses import dataclass, fields
from typing import ClassVar, Self

from sql_smith.functions import alias
from sql_smith.functions import field as sql_field
from sql_smith.interfaces import ExpressionInterface

from kwai.core.db.database import Record


def _validate_dataclass(t):
    """Check if all fields contains data with the correct type.

    A ValueError will be raised when the data for a given field contains data with
    an invalid type.
    """
    for k, v in t.__annotations__.items():
        value = getattr(t, k)
        if not isinstance(value, v):
            raise ValueError(f"{k}({value}) of {t} should be of type {v}!")


@dataclass(frozen=True, kw_only=True, slots=True)
class TableRow:
    """A data transfer object for a row of one table.

    The derived class must be a dataclass.
    """

    __table_name__: ClassVar[str]

    @classmethod
    def get_column_alias(cls, name: str, prefix: str | None = None) -> str:
        """Return the alias for a column."""
        prefix = prefix or cls.__table_name__
        return f"{prefix}_{name}"

    @classmethod
    def aliases(cls, prefix: str | None = None) -> list[ExpressionInterface]:
        """Return aliases for all the fields of the dataclass."""
        result = []
        for field in fields(cls):
            result.append(
                alias(
                    f"{cls.__table_name__}.{field.name}",
                    cls.get_column_alias(field.name, prefix),
                )
            )
        return result

    @classmethod
    def column(cls, column_name: str) -> str:
        """Return the column prefixed with the table name."""
        return f"{cls.__table_name__}.{column_name}"

    @classmethod
    def field(cls, column_name: str):
        """Call sql-smith field with the given column.

        short-cut for: field(table.table_name + '.' + column_name)
        """
        return sql_field(cls.column(column_name))

    @classmethod
    def map(cls, row: Record, prefix: str | None = None) -> Self:
        """Map the data of a row to the dataclass.

        A ValueError will be raised when a field contains data with the wrong type.
        """
        values = {}
        for field in fields(cls):
            column_alias = cls.get_column_alias(field.name, prefix)
            values[field.name] = row.get(column_alias)

        instance = cls(**values)  # noqa
        _validate_dataclass(instance)

        return instance


@dataclass(frozen=True, kw_only=True, slots=True)
class JoinedTableRow:
    """A data transfer object for data from multiple tables.

    Each field of the dataclass will represent a table. The name of the field
    will be used as prefix for creating an alias for each column of the associated
    table.

    The derived class must be a dataclass.
    """

    @classmethod
    def get_aliases(cls) -> list[ExpressionInterface]:
        """Return fields of all the TableRow dataclasses as aliases.

        The name of the field will be used as prefix for the alias.
        """
        assert len(fields(cls)) > 0, "There are no fields. Is this a dataclass?"

        aliases = []
        for field in fields(cls):
            aliases.extend(field.type.aliases(field.name))
        return aliases

    @classmethod
    def map(cls, row: Record) -> Self:
        """Map all fields of this dataclass to the TableRow dataclasses."""
        tables = {}
        for table_field in fields(cls):
            tables[table_field.name] = table_field.type.map(row, table_field.name)
        return cls(**tables)  # noqa
