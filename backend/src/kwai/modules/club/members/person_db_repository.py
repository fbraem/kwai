"""Module that implements a person repository for a database."""

from dataclasses import dataclass

from sql_smith.functions import alias, on

from kwai.core.db.database import Database
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.entity import Entity
from kwai.modules.club.members.contact_db_repository import ContactDbRepository
from kwai.modules.club.members.member_tables import ContactRow, CountryRow, PersonRow
from kwai.modules.club.members.person import PersonEntity, PersonIdentifier
from kwai.modules.club.members.person_repository import (
    PersonNotFoundException,
    PersonRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class PersonQueryRow(JoinedTableRow):
    """A data transfer object for a Contact query."""

    person: PersonRow
    contact: ContactRow
    country: CountryRow
    nationality: CountryRow

    def create_entity(self) -> PersonEntity:
        """Create a Contact entity from a row."""
        return self.person.create_entity(
            self.nationality.create_country(),
            self.contact.create_entity(self.country.create_country()),
        )


class PersonDbRepository(PersonRepository):
    """A person repository for a database."""

    def __init__(self, database: Database):
        self._database = database

    async def create(self, person: PersonEntity) -> PersonEntity:
        if person.contact.id.is_empty():
            new_contact = await ContactDbRepository(self._database).create(
                person.contact
            )
            person = Entity.replace(person, contact=new_contact)
        new_id = await self._database.insert(
            PersonRow.__table_name__, PersonRow.persist(person)
        )
        return Entity.replace(person, id_=PersonIdentifier(new_id))

    async def update(self, person: PersonEntity) -> PersonEntity:
        await ContactDbRepository(self._database).update(person.contact)
        await self._database.update(
            person.id.value, PersonRow.__table_name__, PersonRow.persist(person)
        )

    async def delete(self, person: PersonEntity):
        await ContactDbRepository(self._database).delete(person.contact)
        await self._database.delete(person.id.value, PersonRow.__table_name__)

    async def get(self, id_: PersonIdentifier) -> PersonEntity:
        query = Database.create_query_factory().select()
        query.from_(PersonRow.__table_name__).columns(
            *PersonQueryRow.get_aliases()
        ).inner_join(
            ContactRow.__table_name__,
            on(ContactRow.column("id"), PersonRow.column("contact_id")),
        ).inner_join(
            CountryRow.__table_name__,
            on(CountryRow.column("id"), ContactRow.column("country_id")),
        ).inner_join(
            alias(CountryRow.__table_name__, "nationality"),
            on("nationality.id", PersonRow.column("nationality_id")),
        ).where(
            PersonRow.field("id").eq(id_.value)
        )

        row = await self._database.fetch_one(query)
        if row:
            return PersonQueryRow.map(row).create_entity()

        raise PersonNotFoundException(f"Person with {id_} not found")
