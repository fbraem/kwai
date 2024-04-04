"""Module for defining a member repository using a database."""

from typing import AsyncGenerator

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.club.members.member import MemberEntity, MemberIdentifier
from kwai.modules.club.members.member_db_query import MemberDbQuery, MemberQueryRow
from kwai.modules.club.members.member_query import MemberQuery
from kwai.modules.club.members.member_repository import (
    MemberNotFoundException,
    MemberRepository,
)
from kwai.modules.club.members.member_tables import MemberRow
from kwai.modules.club.members.person_db_repository import PersonDbRepository


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
    ) -> AsyncGenerator[MemberEntity, None]:
        query = query or self.create_query()

        async for row in query.fetch(limit, offset):
            yield MemberQueryRow.map(row).create_entity()

    async def get(self, query: MemberQuery | None = None) -> MemberEntity:
        member_iterator = self.get_all(query)
        try:
            return await anext(member_iterator)
        except StopAsyncIteration:
            raise MemberNotFoundException("Member not found") from None

    async def create(self, member: MemberEntity) -> MemberEntity:
        # When there is no person id, create it.
        if member.person.id.is_empty():
            person = PersonDbRepository(self._database).create(member.person)
            member = Entity.replace(member, person=person)

        new_id = await self._database.insert(
            MemberRow.__table_name__, MemberRow.persist(member)
        )

        return Entity.replace(member, id_=MemberIdentifier(new_id))

    async def update(self, member: MemberEntity) -> None:
        # Update the member
        await self._database.update(
            member.id.value, MemberRow.__table_name__, MemberRow.persist(member)
        )
        # Update person information
        await PersonDbRepository(self._database).update(member.person)

    async def delete(self, member: MemberEntity) -> None:
        await PersonDbRepository(self._database).delete(member.person)
        await self._database.delete(member.id, MemberRow.__table_name__)
