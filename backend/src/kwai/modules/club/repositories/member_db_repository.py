"""Module for defining a member repository using a database."""

from typing import AsyncGenerator

from sql_smith.functions import field

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.club.domain.file_upload import FileUploadEntity
from kwai.modules.club.domain.member import MemberEntity, MemberIdentifier
from kwai.modules.club.repositories._tables import MemberRow, MemberUploadRow
from kwai.modules.club.repositories.member_db_query import MemberDbQuery, MemberQueryRow
from kwai.modules.club.repositories.member_query import MemberQuery
from kwai.modules.club.repositories.member_repository import (
    MemberNotFoundException,
    MemberRepository,
)
from kwai.modules.club.repositories.person_db_repository import PersonDbRepository


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
            person = await PersonDbRepository(self._database).create(member.person)
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

    async def activate_members(self, upload: FileUploadEntity) -> None:
        member_upload_query = (
            self._database.create_query_factory()
            .select("member_id")
            .from_(MemberUploadRow.__table_name__)
            .where(field("import_id").eq(upload.id.value))
        )
        update_query = (
            self._database.create_query_factory()
            .update(MemberRow.__table_name__, {"active": 1})
            .where(field("id").in_(member_upload_query))
        )
        await self._database.execute(update_query)

    async def deactivate_members(self, upload: FileUploadEntity) -> None:
        member_upload_query = (
            self._database.create_query_factory()
            .select("member_id")
            .from_(MemberUploadRow.__table_name__)
            .where(field("import_id").eq(upload.id.value))
        )
        update_query = (
            self._database.create_query_factory()
            .update(MemberRow.__table_name__, {"active": 0})
            .where(field("id").not_in(member_upload_query))
        )
        await self._database.execute(update_query)
