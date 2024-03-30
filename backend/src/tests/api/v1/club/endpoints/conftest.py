"""Module that defines fixtures for testing the club endpoints."""

from typing import AsyncGenerator

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.club.members.contact import ContactEntity
from kwai.modules.club.members.country import CountryEntity
from kwai.modules.club.members.country_db_repository import CountryDbRepository
from kwai.modules.club.members.member import MemberEntity
from kwai.modules.club.members.member_db_repository import MemberDbRepository
from kwai.modules.club.members.person import PersonEntity
from kwai.modules.club.members.value_objects import (
    Address,
    Birthdate,
    Gender,
    License,
)


@pytest.fixture
async def country(database: Database) -> CountryEntity:
    """A fixture for a country."""
    repo = CountryDbRepository(database)
    return await repo.get_by_iso_2("JP")


@pytest.fixture
async def member_entity(
    database: Database, country: CountryEntity
) -> AsyncGenerator[MemberEntity, None]:
    """A fixture for a member in the database."""
    repo = MemberDbRepository(database)
    member = await repo.create(
        MemberEntity(
            license=License(number="12345678", end_date=Date.today().add(years=1)),
            person=PersonEntity(
                name=Name(first_name="Jigoro", last_name="Kano"),
                gender=Gender.MALE,
                birthdate=Birthdate(Date.create(year=1860, month=10, day=28)),
                contact=ContactEntity(
                    emails=[EmailAddress("jigoro.kano@kwai.com")],
                    address=Address(
                        address="",
                        postal_code="",
                        city="Tokyo",
                        county="",
                        country=country,
                    ),
                ),
                nationality=country,
            ),
        )
    )

    yield member

    await repo.delete(member)