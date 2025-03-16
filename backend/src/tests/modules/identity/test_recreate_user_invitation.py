"""Module for testing the recreate user invitation use case."""

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.recreate_user_invitation import (
    RecreateUserInvitation,
    RecreateUserInvitationCommand,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_db_repository import UserDbRepository


async def test_recreate_user_invitation(
    database: Database,
    user: UserEntity,
    publisher,
    make_user_invitation,
    make_user_invitation_in_db,
):
    """Test recreate user invitation."""
    user_invitation = await make_user_invitation_in_db(
        user_invitation=make_user_invitation(
            email=EmailAddress(email="anton.geesink@kwai.com"),
            name=Name(first_name="Anton", last_name="Geesink"),
            user=user,
        )
    )
    user_invitation_repo = UserInvitationDbRepository(database)
    async with UnitOfWork(database):
        new_user_invitation = await RecreateUserInvitation(
            user,
            UserDbRepository(database),
            user_invitation_repo,
            publisher,
        ).execute(RecreateUserInvitationCommand(uuid=str(user_invitation.uuid)))
    assert new_user_invitation is not None, "There should be a user invitation"

    async with UnitOfWork(database):
        await user_invitation_repo.delete(new_user_invitation)

    old_user_invitation = await user_invitation_repo.get_invitation_by_id(
        user_invitation.id
    )
    assert old_user_invitation.revoked, "Old user invitation should be revoked"
