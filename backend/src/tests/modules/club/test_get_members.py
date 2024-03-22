"""Module for testing the use case 'Get Members'."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.club.get_members import GetMembers, GetMembersCommand
from kwai.modules.club.members.member_db_repository import MemberDbRepository
from kwai.modules.club.members.member_repository import MemberRepository


@pytest.fixture
def member_repo(database: Database) -> MemberRepository:
    """A fixture for a member repository."""
    return MemberDbRepository(database)


async def test_get_members(member_repo: MemberRepository):
    """Test get members."""
    command = GetMembersCommand()
    result = await GetMembers(member_repo).execute(command)
    assert result is not None, "There should be a result"


async def test_get_members_with_license_date(member_repo: MemberRepository):
    """Test get members with a license date."""
    command = GetMembersCommand(license_end_month=1)
    result = await GetMembers(member_repo).execute(command)
    assert result is not None, "There should be a result"
