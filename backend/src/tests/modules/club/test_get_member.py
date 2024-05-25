"""Module for testing the use case 'Get Member'."""

import pytest
from kwai.core.db.database import Database
from kwai.core.domain.presenter import Presenter
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.get_member import GetMember, GetMemberCommand
from kwai.modules.club.repositories.member_db_repository import MemberDbRepository
from kwai.modules.club.repositories.member_repository import MemberRepository


class TestPresenter(Presenter[MemberEntity]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        super().__init__()
        self._entity = None

    @property
    def entity(self):
        """Return the entity."""
        return self._entity

    def present(self, use_case_result: MemberEntity) -> None:
        self._entity = use_case_result


@pytest.fixture
def member_repo(database: Database) -> MemberRepository:
    """A fixture for a member repository."""
    return MemberDbRepository(database)


async def test_get_member(member_repo: MemberRepository, make_member_in_db):
    """Test the get member use case."""
    member = await make_member_in_db()
    presenter = TestPresenter()
    command = GetMemberCommand(uuid=str(member.uuid))
    await GetMember(member_repo, presenter).execute(command)
    assert presenter.entity is not None, "The member should exist"
    assert presenter.entity.uuid == member.uuid, "The member should be found"
