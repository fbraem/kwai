"""Module that implements an AuthorRepository for a database."""

from kwai.core.db.database import Database
from kwai.modules.portal.domain.author import AuthorEntity
from kwai.modules.portal.repositories._tables import AuthorRow
from kwai.modules.portal.repositories.author_repository import (
    AuthorNotFoundException,
    AuthorRepository,
)
from tests.core.domain.test_entity import UserIdentifier


class AuthorDbRepository(AuthorRepository):
    """A author repository for a database."""

    def __init__(self, database: Database):
        self._database = database
        super().__init__()

    async def get(self, id: UserIdentifier) -> AuthorEntity:
        query = (
            self._database.create_query_factory()
            .select()
            .from_(AuthorRow.__table_name__)
            .columns(*AuthorRow.get_aliases())
            .where(AuthorRow.field("user_id").eq(id.value))
        )
        row = await self._database.fetch_one(query)
        if row:
            return AuthorRow.map(row).create_entity()

        raise AuthorNotFoundException()

    async def create(self, author: AuthorEntity) -> AuthorEntity:
        await self._database.insert(AuthorRow.__table_name__, AuthorRow.persist(author))
        return author

    async def delete(self, author: AuthorEntity) -> None:
        await self._database.delete(
            author.id.value, AuthorRow.__table_name__, "user_id"
        )
