"""Tests for the table decorator."""

from dataclasses import dataclass

import pytest
from sql_smith.engine import CommonEngine

from kwai.core.db.table import Table


@dataclass(kw_only=True, frozen=True, slots=True)
class ModelRow:
    """Simple test class that implements a table structure."""

    id: str
    name: str
    age: int


ModelTable = Table("users", ModelRow)


def test_wrong_class():
    """Test if the check for a dataclass works."""
    with pytest.raises(AssertionError):

        class WrongRow:
            """A table must be a dataclass..."""

        Table("users", WrongRow)


def test_create_aliases():
    """Test the creation of column aliases."""
    aliases = ModelTable.aliases()
    assert len(aliases) == 3, "There should be at least 3 aliases"
    assert aliases[0].sql(CommonEngine()) == '"users"."id" AS "users_id"'


def test_column():
    """Test the column method."""
    column = ModelTable.column("name")
    assert column == "users.name"


def test_create_aliases_with_other_table_name():
    """Test the creation of column aliases when the table name is also aliased."""
    aliases = ModelTable.aliases("my_users")
    assert len(aliases) == 3, "There should be at least 3 aliases"
    assert aliases[0].sql(CommonEngine()) == '"my_users"."id" AS "my_users_id"'


def test_map_row():
    """Test map row."""
    row = ModelTable.map_row({"users_id": "1", "users_name": "Jigoro", "users_age": 77})
    assert isinstance(row, ModelRow)
    assert row == ModelRow(id="1", name="Jigoro", age=77)


def test_map_with_call():
    """Test map row using the shortcut (__call__)."""
    row = ModelTable({"users_id": "1", "users_name": "Jigoro", "users_age": 77})
    assert isinstance(row, ModelRow)
    assert row == ModelRow(id="1", name="Jigoro", age=77)
