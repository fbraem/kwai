"""Module for testing the use case 'Create Team Member."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.presenter import Presenter
from kwai.modules.teams.create_team_member import (
    CreateTeamMember,
    CreateTeamMemberCommand,
)
from kwai.modules.teams.domain.team import TeamEntity
from kwai.modules.teams.domain.team_member import TeamMember
from kwai.modules.teams.repositories.member_db_repository import MemberDbRepository
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository

pytestmark = pytest.mark.db


class DummyPresenter(Presenter[tuple[TeamMember, TeamEntity]]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        super().__init__()
        self._team_member = None
        self._team = None

    @property
    def team(self) -> TeamEntity:
        """Return the team entity."""
        return self._team

    @property
    def team_member(self) -> TeamMember:
        """Return the team member."""
        return self._team_member

    def present(self, use_case_result: tuple[TeamMember, TeamEntity]) -> None:
        """Handle use case result."""
        self._team_member = use_case_result[0]
        self._team = use_case_result[1]


async def test_create_team_member(
    database: Database, make_team_in_db, make_team_member_in_db
) -> None:
    """Test the use case 'Create Team Member'."""
    presenter = DummyPresenter()
    team = await make_team_in_db()
    team_member = await make_team_member_in_db()

    command = CreateTeamMemberCommand(
        team_id=team.id.value, member_id=str(team_member.member.uuid)
    )
    await CreateTeamMember(
        TeamDbRepository(database), MemberDbRepository(database), presenter
    ).execute(command)
    assert presenter.team is not None, "The team should be available"
    assert presenter.team_member is not None, "There should be a member"
