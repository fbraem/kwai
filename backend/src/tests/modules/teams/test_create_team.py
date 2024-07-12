"""Module that tests the Create Team use case."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.presenter import Presenter
from kwai.modules.teams.create_team import CreateTeam, CreateTeamCommand
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository

pytestmark = pytest.mark.db


class TestPresenter(Presenter[TeamEntity]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        self._entity = None

    @property
    def entity(self) -> TeamEntity:
        """Return the entity."""
        return self._entity

    def present(self, use_case_result: TeamEntity) -> None:
        self._entity = use_case_result


async def test_create_team(database: Database, make_team) -> None:
    """Test the use case 'Create Team'."""
    presenter = TestPresenter()
    team = make_team()
    command = CreateTeamCommand(
        name=team.name,
        active=team.is_active,
        remark=team.remark,
    )
    await CreateTeam(TeamDbRepository(database), presenter).execute((command))
    assert presenter.entity is not None, "The team should be created"
