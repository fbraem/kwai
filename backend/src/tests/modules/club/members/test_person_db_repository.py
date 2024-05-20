"""Module for testing the person repository for a database."""

import pytest
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.entity import Entity
from kwai.modules.club.repositories.person_db_repository import PersonDbRepository
from kwai.modules.club.repositories.person_repository import (
    PersonNotFoundException,
    PersonRepository,
)

pytestmark = pytest.mark.db


@pytest.fixture
def person_repo(database: Database) -> PersonRepository:
    """A fixture for a person repository."""
    return PersonDbRepository(database)


async def test_create_person(person_repo: PersonRepository, make_person_in_db):
    """Test the creation of a person."""
    person = await make_person_in_db()
    assert not person.id.is_empty(), "There should be a person in the database."


async def test_get_person_by_id(person_repo: PersonRepository, make_person_in_db):
    """Test getting a person with the id."""
    person = await make_person_in_db()
    person = await person_repo.get(person.id)
    assert person is not None, "There should be a person."


async def test_update_person(
    database: Database, person_repo: PersonRepository, make_person_in_db
):
    """Test updating a person."""
    person = await make_person_in_db()
    person = Entity.replace(person, remark="This is updated.")
    async with UnitOfWork(database):
        await person_repo.update(person)
    person = await person_repo.get(person.id)
    assert person.remark == "This is updated.", "The person should be updated."


async def test_delete_person(
    database: Database, person_repo: PersonRepository, make_person_in_db
):
    """Test delete of a person."""
    person = await make_person_in_db()
    async with UnitOfWork(database):
        await person_repo.delete(person)
    with pytest.raises(PersonNotFoundException):
        await person_repo.get(person.id)
