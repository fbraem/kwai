"""Module for testing the use case 'Get Member'."""

import pytest
from kwai.core.db.database import Database
from kwai.modules.club.get_member import GetMember, GetMemberCommand
from kwai.modules.club.repositories.member_db_repository import MemberDbRepository
from kwai.modules.club.repositories.member_repository import MemberRepository


@pytest.fixture
def member_repo(database: Database) -> MemberRepository:
    """A fixture for a member repository."""
    return MemberDbRepository(database)


async def test_get_member(member_repo: MemberRepository, make_member_in_db):
    """Test the get member use case."""
    member = await make_member_in_db()
    command = GetMemberCommand(uuid=str(member.uuid))
    result = await GetMember(member_repo).execute(command)
    assert result.uuid == member.uuid, "The member should be found"
