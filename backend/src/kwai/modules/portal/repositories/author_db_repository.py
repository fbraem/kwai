"""Module that implements an AuthorRepository for a database."""

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorEntity, AuthorIdentifier
from kwai.modules.portal.repositories._tables import AuthorRow
from kwai.modules.portal.repositories.author_db_query import (
    AuthorDbQuery,
    AuthorQueryRow,
)
from kwai.modules.portal.repositories.author_query import AuthorQuery
from kwai.modules.portal.repositories.author_repository import (
    AuthorNotFoundException,
    AuthorRepository,
)


class AuthorDbRepository(AuthorRepository):
    """A author repository for a database."""

    def __init__(self, database: Database):
        self._database = database
        super().__init__()

    def create_query(self) -> AuthorQuery:
        """Create a base query."""
        return AuthorDbQuery(self._database)

    async def get(self, id_: AuthorIdentifier) -> AuthorEntity:
        query = self.create_query().filter_by_id(id_)
        row = await query.fetch_one()
        if row:
            return AuthorQueryRow.map(row).create_entity()

        raise AuthorNotFoundException()

    async def get_by_uuid(self, uuid: UniqueId) -> AuthorEntity:
        query = self.create_query().filter_by_uuid(uuid)
        row = await query.fetch_one()
        if row:
            return AuthorQueryRow.map(row).create_entity()

        raise AuthorNotFoundException()

    async def get_all(self, query=None, limit=0, offset=0):
        query = query or self.create_query()

        async for row in query.fetch(limit, offset):
            yield AuthorQueryRow.map(row).create_entity()

    async def create(self, author: AuthorEntity) -> AuthorEntity:
        await self._database.insert(AuthorRow.__table_name__, AuthorRow.persist(author))
        return author

    async def delete(self, author: AuthorEntity) -> None:
        await self._database.delete(
            author.id.value, AuthorRow.__table_name__, "user_id"
        )
