"""Module for testing TrainingTeamDbQuery."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.training.trainings.training import TrainingIdentifier
from kwai.modules.training.trainings.training_team_db_query import TrainingTeamDbQuery

pytestmark = pytest.mark.db


@pytest.mark.asyncio
async def test_filter_by_training(database: Database):
    """Test filtering on training(s)."""
    query = TrainingTeamDbQuery(database)
    query.filter_by_trainings(TrainingIdentifier(10000))

    result = query.fetch()
    try:
        await anext(result)
    except StopAsyncIteration:
        ok = True
    else:
        ok = True
    assert ok is True, "Query is not executed"


@pytest.mark.asyncio
async def test_fetch_coaches(database: Database):
    """Test filtering on training(s)."""
    query = TrainingTeamDbQuery(database)
    query.filter_by_trainings(TrainingIdentifier(1), TrainingIdentifier(2))

    result = await query.fetch_teams()
    assert result is not None, "There should be a result"
