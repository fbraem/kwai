"""Module that implements a refresh token repository for a database."""
from typing import AsyncIterator

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.modules.identity.tokens.refresh_token import (
    RefreshTokenEntity,
    RefreshTokenIdentifier,
)
from kwai.modules.identity.tokens.refresh_token_db_query import RefreshTokenDbQuery
from kwai.modules.identity.tokens.refresh_token_query import RefreshTokenQuery
from kwai.modules.identity.tokens.refresh_token_repository import (
    RefreshTokenNotFoundException,
    RefreshTokenRepository,
)
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.tokens.token_tables import (
    AccessTokensTable,
    RefreshTokenRow,
    RefreshTokensTable,
)
from kwai.modules.identity.users.user_tables import (
    UserAccountsTable,
)


def _create_entity(row) -> RefreshTokenEntity:
    """Create a refresh token entity from a row."""
    return RefreshTokensTable(row).create_entity(
        AccessTokensTable(row).create_entity(UserAccountsTable(row).create_entity())
    )


class RefreshTokenDbRepository(RefreshTokenRepository):
    """Database repository for the refresh token entity."""

    def __init__(self, database: Database):
        self._database = database

    def create_query(self) -> RefreshTokenQuery:
        return RefreshTokenDbQuery(self._database)

    async def get_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> RefreshTokenEntity:
        query = self.create_query()
        query.filter_by_token_identifier(identifier)

        row = await query.fetch_one()
        if row:
            return _create_entity(row)

        raise RefreshTokenNotFoundException()

    async def get(self, id_: RefreshTokenIdentifier) -> RefreshTokenEntity:
        query = self.create_query()
        query.filter_by_id(id_.value)
        row = await query.fetch_one()
        if row:
            return _create_entity(row)

        raise RefreshTokenNotFoundException()

    async def get_all(
        self,
        query: RefreshTokenDbQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[RefreshTokenEntity]:
        query = query or self.create_query()
        async for row in query.fetch(limit, offset):
            yield _create_entity(row)

    async def create(self, refresh_token: RefreshTokenEntity) -> RefreshTokenEntity:
        new_id = await self._database.insert(
            RefreshTokensTable.table_name, RefreshTokenRow.persist(refresh_token)
        )
        await self._database.commit()
        return Entity.replace(refresh_token, id_=RefreshTokenIdentifier(new_id))

    async def update(self, refresh_token: RefreshTokenEntity):
        await self._database.update(
            refresh_token.id.value,
            RefreshTokensTable.table_name,
            RefreshTokenRow.persist(refresh_token),
        )
        await self._database.commit()
