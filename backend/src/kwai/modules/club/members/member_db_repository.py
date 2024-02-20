"""Module for defining a member repository using a database."""
from typing import Any, AsyncIterator

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.club.members.contact import ContactIdentifier
from kwai.modules.club.members.member import MemberEntity, MemberIdentifier
from kwai.modules.club.members.member_db_query import MemberDbQuery
from kwai.modules.club.members.member_query import MemberQuery
from kwai.modules.club.members.member_repository import MemberRepository
from kwai.modules.club.members.member_tables import (
    ContactRow,
    ContactsTable,
    CountriesTable,
    MemberRow,
    MembersTable,
    PersonRow,
    PersonsTable,
)
from kwai.modules.club.members.person import PersonIdentifier


def _create_entity(row: dict[str, Any]) -> MemberEntity:
    return MembersTable(row).create_entity(
        PersonsTable(row).create_entity(
            CountriesTable.map_row(row, "nationalities").create_country(),
            ContactsTable(row).create_entity(CountriesTable(row).create_country()),
        )
    )


class MemberDbRepository(MemberRepository):
    """A member repository using a database."""

    def __init__(self, database: Database):
        """Initialize the repository.

        Args:
            database: The database for this repository.
        """
        self._database = database

    def create_query(self) -> MemberQuery:
        return MemberDbQuery(self._database)

    async def get_all(
        self,
        query: MemberQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[MemberEntity]:
        query = query or self.create_query()

        async for row in query.fetch(limit, offset):
            yield _create_entity(row)

    async def get(self, query: MemberQuery | None = None) -> MemberEntity | None:
        member_iterator = self.get_all(query)
        try:
            return await anext(member_iterator)
        except StopAsyncIteration:
            return None

    async def create(self, member: MemberEntity) -> MemberEntity:
        # When there is no contact id, create it.
        if member.person.contact.id.is_empty():
            new_contact_id = await self._database.insert(
                ContactsTable.table_name, ContactRow.persist(member.person.contact)
            )
            member = Entity.replace(
                member,
                person=Entity.replace(
                    member.person,
                    contact=Entity.replace(
                        member.person.contact, id_=ContactIdentifier(new_contact_id)
                    ),
                ),
            )

        # When there is no person id, create it.
        if member.person.id.is_empty():
            new_person_id = await self._database.insert(
                PersonsTable.table_name, PersonRow.persist(member.person)
            )
            member = Entity.replace(
                member,
                person=Entity.replace(
                    member.person, id_=PersonIdentifier(new_person_id)
                ),
            )

        new_id = await self._database.insert(
            MembersTable.table_name, MemberRow.persist(member)
        )

        await self._database.commit()

        return Entity.replace(member, id_=MemberIdentifier(new_id))

    async def update(self, member: MemberEntity) -> None:
        # Update the member
        await self._database.update(
            member.id.value, MembersTable.table_name, MemberRow.persist(member)
        )
        # Update person information
        await self._database.update(
            member.person.id.value,
            PersonsTable.table_name,
            PersonRow.persist(member.person),
        )
        # Update contact information
        await self._database.update(
            member.person.contact.id.value,
            ContactsTable.table_name,
            ContactRow.persist(member.person.contact),
        )

        await self._database.commit()

    async def delete(self, member: MemberEntity) -> None:
        pass
