"""Module for testing the contact repository for a database."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.entity import Entity
from kwai.modules.club.members.contact_db_repository import ContactDbRepository
from kwai.modules.club.members.contact_repository import (
    ContactNotFoundException,
    ContactRepository,
)

pytestmark = pytest.mark.db


@pytest.fixture
def contact_repo(database: Database) -> ContactRepository:
    """A fixture for a contact repository."""
    return ContactDbRepository(database)


async def test_create_contact(make_contact_in_db):
    """Test creating a contact."""
    contact = await make_contact_in_db()
    assert not contact.id.is_empty(), "Contact should be saved"


async def test_get_contact_by_id(contact_repo: ContactRepository, make_contact_in_db):
    """Test getting the contact with the id."""
    contact = await make_contact_in_db()
    contact = await contact_repo.get(contact.id)
    assert contact is not None, "Contact should be returned"


async def test_update_contact(contact_repo: ContactRepository, make_contact_in_db):
    """Test updating a contact."""
    contact = await make_contact_in_db()
    contact = Entity.replace(contact, remark="This is an update")
    await contact_repo.update(contact)
    contact = await contact_repo.get(contact.id)
    assert contact.remark == "This is an update", "The contact should be updated."


async def test_delete_contact(
    database: Database, contact_repo: ContactRepository, make_contact_in_db
):
    """Test delete of a contact."""
    contact = await make_contact_in_db()
    async with UnitOfWork(database):
        await contact_repo.delete(contact)
    with pytest.raises(ContactNotFoundException):
        await contact_repo.get(contact.id)
