"""Module that implements a refresh token repository for a database."""
import dataclasses
from typing import Iterator

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.refresh_token import (
    RefreshTokenIdentifier,
    RefreshTokenEntity,
)
from kwai.modules.identity.tokens.refresh_token_db_query import RefreshTokenDbQuery
from kwai.modules.identity.tokens.refresh_token_query import RefreshTokenQuery
from kwai.modules.identity.tokens.refresh_token_repository import (
    RefreshTokenRepository,
    RefreshTokenNotFoundException,
)
from kwai.modules.identity.tokens.token_identifier import TokenIdentifier
from kwai.modules.identity.tokens.token_tables import (
    RefreshTokensTable,
    AccessTokensTable,
    RefreshTokenMapper,
    AccessTokenMapper,
)
from kwai.modules.identity.users.user_tables import (
    UserAccountMapper,
    UserAccountsTable,
)


def map_refresh_token(row) -> RefreshTokenEntity:
    """Create a refresh token entity from a row."""
    # pylint: disable=no-member
    return RefreshTokenMapper(
        refresh_token_table=RefreshTokensTable.map_row(row),
        access_token_mapper=AccessTokenMapper(
            access_token_table=AccessTokensTable.map_row(row),
            user_account_mapper=UserAccountMapper(
                user_accounts_table=UserAccountsTable.map_row(row)
            ),
        ),
    ).create_entity()


class RefreshTokenDbRepository(RefreshTokenRepository):
    """Database repository for the refresh token entity."""

    def __init__(self, database: Database):
        self._database = database

    def create_query(self) -> RefreshTokenQuery:
        return RefreshTokenDbQuery(self._database)

    def get_by_token_identifier(
        self, identifier: TokenIdentifier
    ) -> RefreshTokenEntity:
        query = self.create_query()
        query.filter_by_token_identifier(identifier)

        row = query.fetch_one()
        if row:
            return map_refresh_token(row)

        raise RefreshTokenNotFoundException()

    def get(self, id_: int) -> RefreshTokenEntity:
        query = self.create_query()
        query.filter_by_id(id_)
        row = query.fetch_one()
        if row:
            return map_refresh_token(row)

        raise RefreshTokenNotFoundException()

    def get_all(
        self,
        query: RefreshTokenDbQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> Iterator[RefreshTokenEntity]:
        query = query or self.create_query()
        for row in query.fetch(limit, offset):
            yield map_refresh_token(row)

    def create(self, refresh_token: RefreshTokenEntity) -> RefreshTokenEntity:
        record = dataclasses.asdict(RefreshTokensTable.persist(refresh_token))
        del record["id"]
        query = (
            self._database.create_query_factory()
            .insert(RefreshTokensTable.__table_name__)  # pylint: disable=no-member
            .columns(*record.keys())
            .values(*record.values())
        )
        last_insert_id = self._database.execute(query)
        self._database.commit()
        return dataclasses.replace(
            refresh_token, id=RefreshTokenIdentifier(last_insert_id)
        )

    def update(self, refresh_token_entity: RefreshTokenEntity):
        pass
