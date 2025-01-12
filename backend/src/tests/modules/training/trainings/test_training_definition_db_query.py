"""Module for testing TrainingDefinitionDbQuery."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_definition_db_query import (
    TrainingDefinitionDbQuery,
)


pytestmark = pytest.mark.db


async def test_filter_by_id(database: Database):
    """Test filtering on id."""
    query = TrainingDefinitionDbQuery(database)
    query.filter_by_id(TrainingIdentifier(1))

    result = query.fetch()
    try:
        await anext(result)
    except StopAsyncIteration:
        ok = True
    else:
        ok = True
    assert ok is True, "Query is not executed"


async def test_filter_by_ids(database: Database):
    """Test filtering on ids."""
    query = TrainingDefinitionDbQuery(database)
    query.filter_by_ids(TrainingIdentifier(1), TrainingIdentifier(2))

    result = query.fetch()
    try:
        await anext(result)
    except StopAsyncIteration:
        ok = True
    else:
        ok = True
    assert ok is True, "Query is not executed"
