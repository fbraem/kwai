"""Module for defining fixtures of members."""

from typing import Callable, TypeAlias

import pytest
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.domain.person import PersonEntity
from kwai.modules.club.domain.value_objects import License
from kwai.modules.club.repositories.member_db_repository import MemberDbRepository

MemberFixtureFactory: TypeAlias = Callable[[License | None], MemberEntity]


@pytest.fixture
def make_member(make_person) -> MemberFixtureFactory:
    """A factory fixture for a member."""

    def _make_member_entity(
        *,
        license: License | None = None,
        person: PersonEntity | None = None,
        active: bool = True,
    ) -> MemberEntity:
        license = license or License(
            number="12345678", end_date=Date.today().add(years=1)
        )
        person = person or make_person()
        return MemberEntity(license=license, person=person, active=active)

    return _make_member_entity


@pytest.fixture
def make_member_in_db(
    request,
    event_loop,
    database: Database,
    make_member,
    make_person_in_db,
):
    """A fixture for a member in the database."""

    async def _make_member_in_db(member: MemberEntity | None = None) -> MemberEntity:
        member = member or make_member(person=await make_person_in_db())
        repo = MemberDbRepository(database)
        async with UnitOfWork(database):
            member = await repo.create(member)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(member)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return member

    return _make_member_in_db
