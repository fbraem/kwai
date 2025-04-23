"""Module that implements an AuthorRepository for a database."""

from sql_smith.functions import on
from sql_smith.query import SelectQuery

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorEntity, AuthorIdentifier
from kwai.modules.portal.repositories._tables import AuthorRow, UserRow
from kwai.modules.portal.repositories.author_repository import (
    AuthorNotFoundException,
    AuthorRepository,
)


class AuthorDbRepository(AuthorRepository):
    """A author repository for a database."""

    def __init__(self, database: Database):
        self._database = database
        super().__init__()

    def _create_query(self) -> SelectQuery:
        """Create a base query."""
        return (
            self._database.create_query_factory()
            .select()
            .from_(AuthorRow.__table_name__)
            .columns(*(AuthorRow.get_aliases()) + UserRow.get_aliases())
            .join(
                UserRow.__table_name__,
                on(UserRow.column("id"), AuthorRow.column("user_id")),
            )
        )

    async def get(self, id: AuthorIdentifier) -> AuthorEntity:
        query = self._create_query().where(AuthorRow.field("user_id").eq(id.value))
        row = await self._database.fetch_one(query)
        if row:
            user_row = UserRow.map(row)
            return AuthorRow.map(row).create_entity(
                UniqueId.create_from_string(user_row.uuid)
            )

        raise AuthorNotFoundException()

    async def get_by_uuid(self, uuid: UniqueId) -> AuthorEntity:
        query = self._create_query().where(UserRow.field("uuid").eq(uuid))
        row = await self._database.fetch_one(query)
        if row:
            user_row = UserRow.map(row)
            return AuthorRow.map(row).create_entity(
                UniqueId.create_from_string(user_row.uuid)
            )

        raise AuthorNotFoundException()

    async def create(self, author: AuthorEntity) -> AuthorEntity:
        await self._database.insert(AuthorRow.__table_name__, AuthorRow.persist(author))
        return author

    async def delete(self, author: AuthorEntity) -> None:
        await self._database.delete(
            author.id.value, AuthorRow.__table_name__, "user_id"
        )
