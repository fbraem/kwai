"""Module for testing the use case 'Get Team Members'."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.modules.teams.domain.team_member import MemberEntity
from kwai.modules.teams.get_members import GetMembers, GetMembersCommand
from kwai.modules.teams.repositories.member_db_repository import MemberDbRepository

pytestmark = pytest.mark.db


class DummyPresenter(AsyncPresenter[IterableResult[MemberEntity]]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        super().__init__()
        self._count = 0

    @property
    def count(self):
        """Return the count."""
        return self._count

    async def present(self, use_case_result: IterableResult[MemberEntity]) -> None:
        async for _ in use_case_result.iterator:
            self._count += 1


@pytest.fixture
def team_member_presenter() -> DummyPresenter:
    """A fixture for a team member presenter."""
    return DummyPresenter()


async def test_get_members(
    database: Database, make_team_in_db, make_member_in_db, team_member_presenter
):
    """Test get team members."""
    team = await make_team_in_db()
    await make_member_in_db()
    command = GetMembersCommand(team_id=team.id.value)
    await GetMembers(MemberDbRepository(database), team_member_presenter).execute(
        command
    )
    assert team_member_presenter.count > 0
