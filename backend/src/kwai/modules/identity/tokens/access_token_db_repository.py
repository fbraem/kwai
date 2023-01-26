"""Module that implements an access token repository for a database."""
import dataclasses
from typing import Iterator

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.access_token import (
    AccessTokenIdentifier,
    AccessTokenEntity,
)
from kwai.modules.identity.tokens.access_token_db_query import AccessTokenDbQuery
from kwai.modules.identity.tokens.access_token_query import AccessTokenQuery
from kwai.modules.identity.tokens.access_token_repository import (
    AccessTokenRepository,
    AccessTokenNotFoundException,
)
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.tokens.token_tables import (
    AccessTokenMapper,
    AccessTokensTable,
)
from kwai.modules.identity.users.user_tables import UserAccountsTable, UserAccountMapper


def map_access_token(row) -> AccessTokenEntity:
    """Create an access token entity from a row."""
    return AccessTokenMapper(
        access_token_table=AccessTokensTable.map_row(row),
        user_account_mapper=UserAccountMapper(
            user_accounts_table=UserAccountsTable.map_row(row)
        ),
    ).create_entity()


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
            return map_access_token(row)

        raise AccessTokenNotFoundException

    def get_by_identifier(self, identifier: TokenIdentifier) -> AccessTokenEntity:
        query = self.create_query()
        query.filter_by_token_identifier(identifier)

        row = query.fetch_one()
        if row:
            return map_access_token(row)

        raise AccessTokenNotFoundException

    def get_all(
        self,
        query: AccessTokenQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Iterator[AccessTokenEntity]:
        query = query or self.create_query()
        for row in query.fetch(limit, offset):
            yield map_access_token(row)

    def create(self, access_token: AccessTokenEntity) -> AccessTokenEntity:
        new_id = self._database.insert(AccessTokensTable.persist(access_token))
        self._database.commit()
        return dataclasses.replace(access_token, id=AccessTokenIdentifier(new_id))

    def update(self, access_token: AccessTokenEntity):
        pass
