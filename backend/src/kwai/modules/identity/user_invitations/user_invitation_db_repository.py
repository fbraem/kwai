"""Module that implements a user invitation repository for a database."""
from typing import AsyncIterator

from kwai.core.db.database import Database
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.identity.user_invitations.user_invitation import (
    UserInvitationEntity,
    UserInvitationIdentifier,
)
from kwai.modules.identity.user_invitations.user_invitation_db_query import (
    UserInvitationDbQuery,
)
from kwai.modules.identity.user_invitations.user_invitation_query import (
    UserInvitationQuery,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
    UserInvitationNotFoundException,
)
from kwai.modules.identity.user_invitations.user_invitation_tables import (
    UserInvitationsTable,
    UserInvitationRow,
)
from kwai.modules.identity.users.user_tables import UsersTable


def _create_entity(row) -> UserInvitationEntity:
    """Create a user invitation from a row."""
    return UserInvitationsTable(row).create_entity(UsersTable(row).create_entity())


class UserInvitationDbRepository(UserInvitationRepository):
    """A user invitation repository for a database.

    Attributes:
        _database(Database): the database for this repository.
    """

    def __init__(self, database: Database):
        self._database = database

    def create_query(self) -> UserInvitationQuery:
        return UserInvitationDbQuery(self._database)

    async def get_all(
        self,
        query: UserInvitationQuery,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[UserInvitationEntity]:
        async for row in query.fetch(limit, offset):
            yield _create_entity(row)

    async def get_invitation_by_id(
        self, id_: UserInvitationIdentifier
    ) -> UserInvitationEntity:
        """Get the user invitation with the given id.

        Args:
            id_(UserInvitationIdentifier): The id of a user invitation.

        Returns:
            (UserInvitation): The user invitation with the given id.

        Raises:
            (UserInvitationNotFoundException): when the user invitation with the given
                id does not exist.
        """
        query = self.create_query()
        query.filter_by_id(id_)

        if row := await query.fetch_one():
            return _create_entity(row)

        raise UserInvitationNotFoundException(
            f"User invitation with {id} does not exist."
        )

    async def get_invitation_by_uuid(self, uuid: UniqueId) -> UserInvitationEntity:
        """Get the invitation with the given unique id.

        Args:
            uuid(UniqueId): The unique id of a user invitation.

        Returns:
            (UserInvitation): The user invitation with the given unique id.

        Raises:
            (UserInvitationNotFoundException): when the user invitation with the given
                unique id does not exist.
        """
        query = self.create_query()
        query.filter_by_uuid(uuid)

        if row := await query.fetch_one():
            return _create_entity(row)

        raise UserInvitationNotFoundException(
            f"User invitation with uuid {uuid} does not exist."
        )

    async def create(self, invitation: UserInvitationEntity) -> UserInvitationEntity:
        new_id = await self._database.insert(
            UserInvitationsTable.table_name, UserInvitationRow.persist(invitation)
        )
        await self._database.commit()
        return Entity.replace(invitation, id_=UserInvitationIdentifier(new_id))

    async def update(self, invitation: UserInvitationEntity) -> None:
        await self._database.update(
            invitation.id.value,
            UserInvitationsTable.table_name,
            UserInvitationRow.persist(invitation),
        )
        await self._database.commit()

    async def delete(self, invitation: UserInvitationEntity) -> None:
        await self._database.delete(
            invitation.id.value, UserInvitationsTable.table_name
        )
        await self._database.commit()
