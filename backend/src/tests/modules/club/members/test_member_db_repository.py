"""Module for testing the member database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.members.contact import ContactEntity
from kwai.modules.club.members.country import CountryEntity, CountryIdentifier
from kwai.modules.club.members.member import MemberEntity
from kwai.modules.club.members.member_db_repository import MemberDbRepository
from kwai.modules.club.members.member_repository import MemberRepository
from kwai.modules.club.members.person import PersonEntity
from kwai.modules.club.members.value_objects import (
    Address,
    Birthdate,
    Gender,
    License,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def member_repo(database: Database) -> MemberRepository:
    """A fixture for a member repository."""
    return MemberDbRepository(database)


@pytest.fixture(scope="module")
async def member(member_repo: MemberRepository) -> MemberEntity:
    """Create a member entity."""
    member = MemberEntity(
        uuid=UniqueId.generate(),
        license=License(number="12346789", end_date=Date.today().add(years=1)),
        person=PersonEntity(
            name=Name(first_name="Jigoro", last_name="Kano"),
            gender=Gender.MALE,
            birthdate=Birthdate(Date.create(1860, 10, 28)),
            nationality=CountryEntity(
                id_=CountryIdentifier(84), iso_2="JP", iso_3="JPN", name="Japan"
            ),
            contact=ContactEntity(
                emails=[EmailAddress("jigoro.kano@kwai.com")],
                address=Address(
                    address="",
                    postal_code="",
                    city="Tokyo",
                    county="",
                    country=CountryEntity(
                        id_=CountryIdentifier(84), iso_2="JP", iso_3="JPN", name="Japan"
                    ),
                ),
            ),
        ),
    )
    return await member_repo.create(member)


async def test_create_member(member: MemberEntity):
    """Test create member."""
    assert not member.id.is_empty(), "There should be a member created."


async def test_update_member(member_repo: MemberRepository, member: MemberEntity):
    """Test update member."""
    contact = Entity.replace(
        member.person.contact,
        remark="Update contact from test",
        traceable_time=member.person.contact.traceable_time.mark_for_update(),
    )
    person = Entity.replace(
        member.person,
        remark="Update person from test",
        contact=contact,
        traceable_time=member.person.traceable_time.mark_for_update(),
    )
    member = Entity.replace(
        member,
        remark="Update member from test",
        person=person,
        traceable_time=member.traceable_time.mark_for_update(),
    )

    try:
        await member_repo.update(member)
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")


async def test_get_all(member_repo: MemberRepository):
    """Test get all."""
    try:
        it = member_repo.get_all()
        await anext(it)
    except Exception as exc:
        pytest.fail(f"An exception occurred: {exc}")
