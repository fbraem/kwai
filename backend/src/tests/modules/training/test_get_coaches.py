"""Module for testing the GetCoaches use case."""
from kwai.core.db.database import Database
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.get_coaches import GetCoaches, GetCoachesCommand


async def test_get_coaches(database: Database):
    """Test the get coaches use case."""
    coach_repo = CoachDbRepository(database)
    command = GetCoachesCommand(active=True)
    count, iterator = await GetCoaches(coach_repo).execute(command)
    assert count is not None, "There should be result"
