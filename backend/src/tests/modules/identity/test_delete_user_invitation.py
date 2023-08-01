"""Module for testing the use case GetUserInvitation."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.delete_user_invitation import (
    DeleteUserInvitation,
    DeleteUserInvitationCommand,
)
from kwai.modules.identity.get_user_invitation import (
    GetUserInvitation,
    GetUserInvitationCommand,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationNotFoundException,
    UserInvitationRepository,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Fixture for creating the invitation repository."""
    return UserInvitationDbRepository(database)


@pytest.mark.asyncio
async def test_delete_invitation(
    repo: UserInvitationRepository,
    user_invitation,
):
    """Test the use case: delete user invitation."""
    command = DeleteUserInvitationCommand(uuid=str(user_invitation.uuid))
    await DeleteUserInvitation(repo).execute(command)

    command = GetUserInvitationCommand(uuid=str(user_invitation.uuid))
    with pytest.raises(UserInvitationNotFoundException):
        await GetUserInvitation(repo).execute(command)
