"""Tests for the table decorator."""
from dataclasses import dataclass

import pytest
from sql_smith.engine import CommonEngine

from kwai.core.db.table import table


@table(name="users")
@dataclass(kw_only=True, frozen=True, slots=True)
class ModelTest:
    """Simple test class that implements a table structure."""

    id: str
    name: str
    age: int


def test_wrong_class():
    """Test if the check for a dataclass works."""
    with pytest.raises(AssertionError):

        # pylint: disable=unused-variable,too-few-public-methods
        @table(name="wrong")
        class WrongModel:
            """Using a wrong model..."""


def test_create_aliases():
    """Test the creation of column aliases."""
    # pylint: disable=no-member
    aliases = ModelTest.aliases()
    assert len(aliases) == 3, "There should be at least 3 aliases"
    assert aliases[0].sql(CommonEngine()), '"users"."id" AS "users_id"'


def test_column():
    """Test the column method."""
    column = ModelTest.column("name")
    assert column, "users.name"


def test_create_aliases_with_other_table_name():
    """Test the creation of column aliases when the table name is also aliased."""
    # pylint: disable=no-member
    aliases = ModelTest.aliases("my_users")
    assert len(aliases) == 3, "There should be at least 3 aliases"
    assert aliases[0].sql(CommonEngine()), '"my_users"."id" AS "my_users_id"'
