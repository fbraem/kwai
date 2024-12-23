"""Module for defining factory fixtures for teams."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository


@pytest.fixture
def make_team():
    """A factory fixture for creating a team."""

    def _make_team(name: str | None = None) -> TeamEntity:
        return TeamEntity(name=name or "U11")

    return _make_team


@pytest.fixture
def make_team_in_db(request, event_loop, database: Database, make_team):
    """A factory fixture for creating a team in database."""

    async def _make_team_in_db(team: TeamEntity | None = None) -> TeamEntity:
        team = team or make_team()
        repo = TeamDbRepository(database)
        async with UnitOfWork(database):
            team = await repo.create(team)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(team)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return team

    return _make_team_in_db
