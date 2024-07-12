"""Module for defining tests for the use case 'Get Teams'."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.get_teams import GetTeams, GetTeamsCommand
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository

pytestmark = pytest.mark.db


class TestPresenter(AsyncPresenter[IterableResult[TeamEntity]]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        super().__init__()
        self._count = 0

    @property
    def count(self):
        """Return the count."""
        return self._count

    async def present(self, use_case_result: IterableResult[TeamEntity]) -> None:
        async for _ in use_case_result.iterator:
            self._count += 1


async def test_get_teams(database: Database, make_team_in_db):
    """Test get teams."""
    await make_team_in_db()
    command = GetTeamsCommand()
    presenter = TestPresenter()
    await GetTeams(TeamDbRepository(database), presenter).execute(command)
    print(presenter.count)
    assert presenter.count > 0, "There should be at least one team."
