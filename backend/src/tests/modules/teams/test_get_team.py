"""Module for defining tests for the use case 'Get Teams'."""

from kwai.core.db.database import Database
from kwai.core.domain.presenter import Presenter
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.get_team import GetTeam, GetTeamCommand
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository


class TestPresenter(Presenter[TeamEntity]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        super().__init__()
        self._entity = None

    @property
    def entity(self):
        """Return the entity."""
        return self._entity

    def present(self, use_case_result: TeamEntity) -> None:
        self._entity = use_case_result


async def test_get_teams(database: Database, make_team_in_db):
    """Test get teams."""
    team = await make_team_in_db()
    print(team)
    command = GetTeamCommand(id=team.id.value)
    presenter = TestPresenter()
    await GetTeam(TeamDbRepository(database), presenter).execute(command)
    assert presenter.entity is not None, "The team should exist"
    assert presenter.entity.id == team.id, "The team should be found"
