"""Module for testing the use case 'Get Members'."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.get_members import GetMembers, GetMembersCommand
from kwai.modules.club.members.member_db_repository import MemberDbRepository
from kwai.modules.club.members.member_repository import MemberRepository
from kwai.modules.club.members.value_objects import License


@pytest.fixture
def member_repo(database: Database) -> MemberRepository:
    """A fixture for a member repository."""
    return MemberDbRepository(database)


async def test_get_members(member_repo: MemberRepository, make_member_in_db):
    """Test get members."""
    await make_member_in_db()
    command = GetMembersCommand()
    result = await GetMembers(member_repo).execute(command)
    assert result.count > 0, "There should be at least one member"


async def test_get_members_with_license_date(
    member_repo: MemberRepository, make_member, make_member_in_db, make_person_in_db
):
    """Test get members with a license date."""
    await make_member_in_db(
        make_member(
            license=License(number="0123456789", end_date=Date.create(2023, 2, 28)),
            person=await make_person_in_db(),
        )
    )
    command = GetMembersCommand(license_end_year=2023, license_end_month=2)
    result = await GetMembers(member_repo).execute(command)
    assert result.count == 1, "There should only be one member"
