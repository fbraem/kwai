"""Module that defines a contact repository for a database."""

from dataclasses import dataclass

from sql_smith.functions import on

from kwai.core.db.database import Database
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.entity import Entity
from kwai.modules.club.domain.contact import ContactEntity, ContactIdentifier
from kwai.modules.club.repositories._tables import ContactRow, CountryRow
from kwai.modules.club.repositories.contact_repository import (
    ContactNotFoundException,
    ContactRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class ContactQueryRow(JoinedTableRow):
    """A data transfer object for a Contact query."""

    contact: ContactRow
    country: CountryRow

    def create_entity(self) -> ContactEntity:
        """Create a Contact entity from a row."""
        return self.contact.create_entity(self.country.create_country())


class ContactDbRepository(ContactRepository):
    """A contact repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    async def create(self, contact: ContactEntity) -> ContactEntity:
        new_contact_id = await self._database.insert(
            ContactRow.__table_name__, ContactRow.persist(contact)
        )
        return Entity.replace(contact, id_=ContactIdentifier(new_contact_id))

    async def delete(self, contact: ContactEntity):
        await self._database.delete(contact.id.value, ContactRow.__table_name__)

    async def update(self, contact: ContactEntity):
        await self._database.update(
            contact.id.value, ContactRow.__table_name__, ContactRow.persist(contact)
        )

    async def get(self, id_: ContactIdentifier) -> ContactEntity:
        query = Database.create_query_factory().select()
        query.from_(ContactRow.__table_name__).columns(
            *ContactQueryRow.get_aliases()
        ).inner_join(
            CountryRow.__table_name__,
            on(CountryRow.column("id"), ContactRow.column("country_id")),
        ).where(ContactRow.field("id").eq(id_.value))
        row = await self._database.fetch_one(query)
        if row:
            return ContactQueryRow.map(row).create_entity()

        raise ContactNotFoundException(f"Contact with {id_} not found")
