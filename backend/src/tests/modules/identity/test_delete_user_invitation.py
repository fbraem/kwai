"""Module for testing the use case GetUserInvitation."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.delete_user_invitation import (
    DeleteUserInvitationCommand,
    DeleteUserInvitation,
)
from kwai.modules.identity.get_user_invitation import (
    GetUserInvitationCommand,
    GetUserInvitation,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
    UserInvitationNotFoundException,
)


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Fixture for creating the invitation repository."""
    return InvitationDbRepository(database)


def test_delete_invitation(
    repo: UserInvitationRepository,
    create_user_invitation,
):
    """Test the use case: delete user invitation."""
    user_invitation = create_user_invitation(False)
    command = DeleteUserInvitationCommand(uuid=str(user_invitation.uuid))
    DeleteUserInvitation(repo).execute(command)

    command = GetUserInvitationCommand(uuid=str(user_invitation.uuid))
    with pytest.raises(UserInvitationNotFoundException):
        GetUserInvitation(repo).execute(command)
