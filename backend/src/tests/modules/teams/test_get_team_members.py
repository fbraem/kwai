"""Module for testing the use case 'Get Team Members'."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.modules.teams.domain.team_member import TeamMember
from kwai.modules.teams.get_team_members import GetTeamMembers, GetTeamMembersCommand
from kwai.modules.teams.repositories.member_db_repository import MemberDbRepository

pytestmark = pytest.mark.db


class DummyPresenter(AsyncPresenter[IterableResult[TeamMember]]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        super().__init__()
        self._count = 0

    @property
    def count(self):
        """Return the count."""
        return self._count

    async def present(self, use_case_result: IterableResult[TeamMember]) -> None:
        async for _ in use_case_result.iterator:
            self._count += 1


async def test_get_team_members(
    database: Database, make_team_in_db, make_team_member_in_db
):
    """Test get team members."""
    team = await make_team_in_db()
    await make_team_member_in_db(team=team)
    command = GetTeamMembersCommand(team_id=team.id.value, in_team=True)
    presenter = DummyPresenter()
    await GetTeamMembers(MemberDbRepository(database), presenter).execute(command)
    assert presenter.count > 0


async def test_get_team_members_not_in_team(database: Database, make_team_in_db):
    """Test get team members not in the team."""
    await make_team_in_db()
    command = GetTeamMembersCommand()
    presenter = DummyPresenter()
    await GetTeamMembers(MemberDbRepository(database), presenter).execute(command)
    assert presenter.count > 0
