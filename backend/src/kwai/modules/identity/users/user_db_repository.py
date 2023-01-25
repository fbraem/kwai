"""Module for implementing a user repository with a database."""
from kwai.core.db import Database
from kwai.core.domain.value_objects import UniqueId, EmailAddress
from kwai.modules.identity.users import (
    UserEntity,
    UserNotFoundException,
    UserDbQuery,
    UserRepository,
)
from kwai.modules.identity.users.user_tables import UserMapper, UsersTable


class UserDbRepository(UserRepository):
    """Database repository for the user entity."""

    def __init__(self, database: Database):
        self._database = database

    def create_query(self) -> UserDbQuery:
        """Create a user database query."""
        return UserDbQuery(self._database)

    def get_user_by_id(self, id_: int) -> UserEntity:
        """Get the user with the given id.

        UserNotFoundException is raised when the user does not exist.
        """
        query = self.create_query()
        query.filter_by_id(id_)

        row = query.fetch_one()
        if row:
            return UserMapper(users_table=UsersTable.map_row(row)).create_entity()

        raise UserNotFoundException()

    def get_user_by_uuid(self, uuid: UniqueId) -> UserEntity:
        """Get the user with the given uuid.

        UserNotFoundException is raised when the user does not exist.
        """
        query = self.create_query()
        query.filter_by_uuid(uuid)

        row = query.fetch_one()
        if row:
            return UserMapper(users_table=UsersTable.map_row(row)).create_entity()

        raise UserNotFoundException()

    def get_user_by_email(self, email: EmailAddress) -> UserEntity:
        """Get the user with the given email.

        UserNotFoundException is raised when the user does not exist.
        """
        query = self.create_query()
        query.filter_by_email(email)

        row = query.fetch_one()
        if row:
            return UserMapper(users_table=UsersTable.map_row(row)).create_entity()

        raise UserNotFoundException()
