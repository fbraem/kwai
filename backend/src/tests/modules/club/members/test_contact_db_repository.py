"""Module for testing the contact repository for a database."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.club.members.contact_db_repository import ContactDbRepository
from kwai.modules.club.members.contact_repository import ContactRepository

pytestmark = pytest.mark.db


@pytest.fixture
async def contact_repo(database: Database) -> ContactRepository:
    """A fixture for a contact repository."""
    return ContactDbRepository(database)


async def test_create_contact(make_country_in_db, make_address, make_contact_in_db):
    """Test creating a contact."""
    address = make_address(country=await make_country_in_db())
    contact = await make_contact_in_db(address=address)
    assert not contact.id.is_empty(), "Contact should be saved"
