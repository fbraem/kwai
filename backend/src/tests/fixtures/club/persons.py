"""Module for defining fixtures for persons."""

import pytest
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.date import Date
from kwai.core.domain.value_objects.name import Name
from kwai.modules.club.domain.contact import ContactEntity
from kwai.modules.club.domain.country import CountryEntity
from kwai.modules.club.domain.person import PersonEntity
from kwai.modules.club.domain.value_objects import Birthdate, Gender
from kwai.modules.club.members.person_db_repository import PersonDbRepository


@pytest.fixture
def make_person(make_contact, country_japan):
    """A factory fixture for a person."""

    def _make_person(
        name: Name | None = None,
        gender: Gender | None = None,
        birthdate: Birthdate | None = None,
        nationality: CountryEntity | None = None,
        contact: ContactEntity | None = None,
    ) -> PersonEntity:
        return PersonEntity(
            name=name or Name(first_name="Jigoro", last_name="Kano"),
            gender=gender or Gender.MALE,
            birthdate=birthdate or Birthdate(Date.create(year=1860, month=10, day=28)),
            nationality=nationality or country_japan,
            contact=contact or make_contact(),
        )

    return _make_person


@pytest.fixture
def make_person_in_db(
    request,
    event_loop,
    database: Database,
    make_person,
    make_contact_in_db,
    make_country_in_db,
    country_japan,
):
    """A factory fixture for a person in a database."""

    async def _make_person_in_db(person: PersonEntity | None = None) -> PersonEntity:
        person = person or make_person(
            contact=await make_contact_in_db(),
            nationality=await make_country_in_db(country_japan),
        )
        repo = PersonDbRepository(database)
        async with UnitOfWork(database):
            person = await repo.create(person)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(person)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return person

    return _make_person_in_db
