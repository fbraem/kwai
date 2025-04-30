"""Module that implements an AuthorQuery for a database."""

from dataclasses import dataclass
from typing import Self

from sql_smith.functions import on

from kwai.core.db.database import Database
from kwai.core.db.database_query import DatabaseQuery
from kwai.core.db.table_row import JoinedTableRow
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.portal.domain.author import AuthorEntity
from kwai.modules.portal.repositories._tables import AuthorRow, UserRow
from kwai.modules.portal.repositories.author_query import AuthorQuery


@dataclass(kw_only=True, frozen=True, slots=True)
class AuthorQueryRow(JoinedTableRow):
    """A data transfer object for the author query."""

    author: AuthorRow
    user: UserRow

    def create_entity(self) -> AuthorEntity:
        """Create an Author entity from a row."""
        return self.author.create_entity(
            uuid=UniqueId.create_from_string(self.user.uuid)
        )


class AuthorDbQuery(AuthorQuery, DatabaseQuery):
    """An author query using a database."""

    def __init__(self, database: Database):
        super().__init__(database)

    def init(self):
        self._query.from_(AuthorRow.__table_name__).columns(
            *(AuthorRow.get_aliases()) + UserRow.get_aliases()
        ).join(
            UserRow.__table_name__,
            on(UserRow.column("id"), AuthorRow.column("user_id")),
        )

    @property
    def columns(self):
        return AuthorQueryRow.get_aliases()

    def filter_by_id(self, id_) -> Self:
        self._query.and_where(AuthorRow.field("user_id").eq(id_.value))
        return self

    def filter_by_uuid(self, uuid: UniqueId):
        self._query.and_where(UserRow.field("uuid").eq(uuid))
        return self
