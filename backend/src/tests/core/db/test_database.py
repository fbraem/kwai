"""Module for testing Database class."""
import pytest
from sql_smith.functions import alias, func
from sql_smith.query import SelectQuery

from kwai.core.db.database import Database

pytestmark = pytest.mark.db


async def test_fetch(database: Database):
    """Test fetch."""
    select: SelectQuery = (
        Database.create_query_factory()
        .select(alias(func("COUNT", func("DISTINCT", "email")), "c"))
        .from_("users")
    )
    record = await database.fetch_one(select)
    assert record is not None, "There should be at least a record"
    assert "c" in record, "There should be a key 'c' in the record"
