"""Module that implements an access token repository for a database."""
from typing import Iterator, Any

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.identity.tokens.access_token import (
    AccessTokenEntity,
    AccessTokenIdentifier,
)
from kwai.modules.identity.tokens.access_token_db_query import AccessTokenDbQuery
from kwai.modules.identity.tokens.access_token_query import AccessTokenQuery
from kwai.modules.identity.tokens.access_token_repository import (
    AccessTokenNotFoundException,
    AccessTokenRepository,
)
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.tokens.token_tables import (
    AccessTokensTable,
    AccessTokenRow,
)
from kwai.modules.identity.users.user_tables import UserAccountsTable


def _create_entity(row: dict[str, Any]) -> AccessTokenEntity:
    """Create an access token entity from a row."""
    return AccessTokensTable(row).create_entity(UserAccountsTable(row).create_entity())


class AccessTokenDbRepository(AccessTokenRepository):
    """Database repository for the access token entity."""

    def __init__(self, database: Database):
        self._database = database

    def create_query(self) -> AccessTokenQuery:
        return AccessTokenDbQuery(self._database)

    def get(self, id_: AccessTokenIdentifier) -> AccessTokenEntity:
        query = self.create_query()
        query.filter_by_id(id_.value)

        row = query.fetch_one()
        if row:
            return _create_entity(row)

        raise AccessTokenNotFoundException

    def get_by_identifier(self, identifier: TokenIdentifier) -> AccessTokenEntity:
        query = self.create_query()
        query.filter_by_token_identifier(identifier)

        row = query.fetch_one()
        if row:
            return _create_entity(row)

        raise AccessTokenNotFoundException

    def get_all(
        self,
        query: AccessTokenQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Iterator[AccessTokenEntity]:
        query = query or self.create_query()
        for row in query.fetch(limit, offset):
            yield _create_entity(row)

    def create(self, access_token: AccessTokenEntity) -> AccessTokenEntity:
        new_id = self._database.insert(
            AccessTokensTable.table_name, AccessTokenRow.persist(access_token)
        )
        self._database.commit()
        return Entity.replace(access_token, id_=AccessTokenIdentifier(new_id))

    def update(self, access_token: AccessTokenEntity):
        self._database.update(
            access_token.id.value,
            AccessTokensTable.table_name,
            AccessTokenRow.persist(access_token),
        )
        self._database.commit()
