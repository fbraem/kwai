"""Module for testing the GetCoaches use case."""

from kwai.core.db.database import Database
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.get_coaches import GetCoaches, GetCoachesCommand


async def test_get_coaches(database: Database, make_coach_in_db):
    """Test the get coaches use case."""
    coach = await make_coach_in_db()

    command = GetCoachesCommand(active=True)
    coach_repo = CoachDbRepository(database)
    count, iterator = await GetCoaches(coach_repo).execute(command)
    assert count > 0, "There should be at least one result"

    coaches = {coach.id: coach async for coach in iterator}
    assert coach.id in coaches, "The coach should be retrieved"
