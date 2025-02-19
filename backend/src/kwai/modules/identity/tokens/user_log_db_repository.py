"""Module that defines a User Log repository for a database."""

from kwai.core.db.database import Database
from kwai.modules.identity.tokens.token_tables import UserLogRow
from kwai.modules.identity.tokens.user_log import UserLogEntity, UserLogIdentifier
from kwai.modules.identity.tokens.user_log_repository import UserLogRepository


class UserLogDbRepository(UserLogRepository):
    """Class that represents a User Log repository for a database."""

    def __init__(self, database: Database):
        self._db = database

    async def create(self, user_log: UserLogEntity) -> UserLogEntity:
        new_id = await self._db.insert(
            UserLogRow.__table_name__, UserLogRow.persist(user_log)
        )
        return user_log.set_id(UserLogIdentifier(new_id))
