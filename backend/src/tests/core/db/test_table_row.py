"""Module for testing the data transfer objects TableRow and TableJoinRow."""

from dataclasses import dataclass

import pytest
from sql_smith.engine import CommonEngine

from kwai.core.db.table_row import JoinedTableRow, TableRow


@dataclass(kw_only=True, frozen=True, slots=True)
class JudokaRow(TableRow):
    """Data transfer object for a row of the judokas table."""

    __table_name__ = "judokas"

    id: int
    name: str
    age: int


def test_aliases():
    """Test if the aliases are created correctly."""
    aliases = JudokaRow.get_aliases()
    assert len(aliases) == 3, "There should be 3 aliases."
    assert aliases[0].sql(CommonEngine()) == '"judokas"."id" AS "judokas_id"'
    assert aliases[1].sql(CommonEngine()) == '"judokas"."name" AS "judokas_name"'
    assert aliases[2].sql(CommonEngine()) == '"judokas"."age" AS "judokas_age"'


def test_column():
    """Test if the column is created correctly."""
    column = JudokaRow.column("name")
    assert column == "judokas.name"


def test_create_aliases_with_other_table_name():
    """Test the creation of column aliases when the table name is also aliased."""
    aliases = JudokaRow.get_aliases("my_judokas")
    assert len(aliases) == 3, "There should be 3 aliases"
    assert aliases[0].sql(CommonEngine()) == '"judokas"."id" AS "my_judokas_id"'
    assert aliases[1].sql(CommonEngine()) == '"judokas"."name" AS "my_judokas_name"'
    assert aliases[2].sql(CommonEngine()) == '"judokas"."age" AS "my_judokas_age"'


def test_map_row():
    """Test map row."""
    row = JudokaRow.map({"judokas_id": 1, "judokas_name": "Jigoro", "judokas_age": 77})
    assert row == JudokaRow(id=1, name="Jigoro", age=77)


def test_invalid_map_row():
    """Test map row."""
    with pytest.raises(ValueError, match=r"^id\(1\) of JudokaRow"):
        JudokaRow.map({"judokas_id": "1", "judokas_name": "Jigoro", "judokas_age": 77})


@dataclass(kw_only=True, frozen=True, slots=True)
class CountryRow(TableRow):
    """Data transfer object for a row of the countries table."""

    __table_name__ = "countries"

    iso_2: str
    name: str


@dataclass(kw_only=True, frozen=True, slots=True)
class MemberRow(JoinedTableRow):
    """A data transfer object for a query that joins multiple tables.."""

    judoka: JudokaRow
    country: CountryRow


def test_joined_table_row():
    """Test JoinedTableRow."""
    aliases = MemberRow.get_aliases()
    assert len(aliases) == 5, "There should be 5 aliases."
    assert aliases[0].sql(CommonEngine()) == '"judokas"."id" AS "judoka_id"'
    assert aliases[1].sql(CommonEngine()) == '"judokas"."name" AS "judoka_name"'
    assert aliases[2].sql(CommonEngine()) == '"judokas"."age" AS "judoka_age"'
    assert aliases[3].sql(CommonEngine()) == '"countries"."iso_2" AS "country_iso_2"'
    assert aliases[4].sql(CommonEngine()) == '"countries"."name" AS "country_name"'


def test_map_joined_tables():
    """Test mapping from a row with joined tables."""
    row = MemberRow.map(
        {
            "judoka_id": 1,
            "judoka_name": "Jigoro",
            "judoka_age": 77,
            "country_iso_2": "JP",
            "country_name": "Japan",
        }
    )
    assert row.judoka == JudokaRow(id=1, name="Jigoro", age=77)
    assert row.country == CountryRow(iso_2="JP", name="Japan")
