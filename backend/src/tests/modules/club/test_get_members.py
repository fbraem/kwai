"""Module for testing the use case 'Get Members'."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.domain.value_objects import License
from kwai.modules.club.get_members import GetMembers, GetMembersCommand
from kwai.modules.club.repositories.member_db_repository import MemberDbRepository
from kwai.modules.club.repositories.member_repository import MemberRepository


class DummyPresenter(AsyncPresenter[IterableResult[MemberEntity]]):
    """A dummy presenter for checking the use case result."""

    def __init__(self):
        super().__init__()
        self._count = 0

    @property
    def count(self):
        """Return count."""
        return self._count

    async def present(self, use_case_result: IterableResult[MemberEntity]) -> None:
        """Process the result of the use case."""
        self._count += 1


@pytest.fixture
def member_repo(database: Database) -> MemberRepository:
    """A fixture for a member repository."""
    return MemberDbRepository(database)


async def test_get_members(member_repo: MemberRepository, make_member_in_db):
    """Test get members."""
    await make_member_in_db()
    command = GetMembersCommand()
    presenter = DummyPresenter()
    await GetMembers(member_repo, presenter).execute(command)
    assert presenter.count > 0, "There should be at least one member"


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
    presenter = DummyPresenter()
    await GetMembers(member_repo, presenter).execute(command)
    assert presenter.count == 1, "There should only be one member"


async def test_get_all_members(
    member_repo: MemberRepository, make_member, make_member_in_db, make_person_in_db
):
    """Test get members to include inactive members."""
    await make_member_in_db(
        make_member(
            active=False,
            person=await make_person_in_db(),
        )
    )
    command = GetMembersCommand(active=False)
    presenter = DummyPresenter()
    await GetMembers(member_repo, presenter).execute(command)
    assert presenter.count > 0, "There should be at least one inactive member"
