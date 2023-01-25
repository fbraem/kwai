"""Tests for the table decorator."""
from dataclasses import dataclass

import pytest
from sql_smith.engine import CommonEngine

from kwai.core.db import table


@table(name="users")
@dataclass(kw_only=True, frozen=True, slots=True)
class TestModel:
    id: str
    name: str
    age: int


def test_wrong_class():
    with pytest.raises(RuntimeError):

        @table(name="wrong")
        class WrongModel:
            pass


def test_create_aliases():
    aliases = TestModel.aliases()
    assert len(aliases) == 3, "There should be at least 3 aliases"
    assert aliases[0].sql(CommonEngine()), '"users"."id" AS "users_id"'


def test_create_aliases_with_other_table_name():
    aliases = TestModel.aliases("my_users")
    assert len(aliases) == 3, "There should be at least 3 aliases"
    assert aliases[0].sql(CommonEngine()), '"my_users"."id" AS "my_users_id"'
