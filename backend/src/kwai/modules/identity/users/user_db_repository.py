"""Module for implementing a user repository with a database."""

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.users.user import UserEntity, UserIdentifier
from kwai.modules.identity.users.user_db_query import UserDbQuery
from kwai.modules.identity.users.user_repository import (
    UserNotFoundException,
    UserRepository,
)
from kwai.modules.identity.users.user_tables import UserRow


class UserDbRepository(UserRepository):
    """Database repository for the user entity."""

    def __init__(self, database: Database):
        self._database = database

    async def update(self, user: UserEntity) -> None:
        await self._database.update(
            user.id.value, UserRow.__table_name__, UserRow.persist(user)
        )

    def create_query(self) -> UserDbQuery:
        """Create a user database query."""
        return UserDbQuery(self._database)

    async def get_user_by_id(self, id_: UserIdentifier) -> UserEntity:
        """Get the user with the given id.

        UserNotFoundException is raised when the user does not exist.
        """
        query = self.create_query()
        query.filter_by_id(id_)

        row = await query.fetch_one()
        if row:
            return UserRow.map(row).create_entity()

        raise UserNotFoundException()

    async def get_user_by_uuid(self, uuid: UniqueId) -> UserEntity:
        """Get the user with the given uuid.

        UserNotFoundException is raised when the user does not exist.
        """
        query = self.create_query()
        query.filter_by_uuid(uuid)

        row = await query.fetch_one()
        if row:
            return UserRow.map(row).create_entity()

        raise UserNotFoundException()

    async def get_user_by_email(self, email: EmailAddress) -> UserEntity:
        """Get the user with the given email.

        UserNotFoundException is raised when the user does not exist.
        """
        query = self.create_query()
        query.filter_by_email(email)

        row = await query.fetch_one()
        if row:
            return UserRow.map(row).create_entity()

        raise UserNotFoundException()
