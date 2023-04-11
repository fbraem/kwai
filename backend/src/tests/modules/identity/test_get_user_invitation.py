"""Module for testing the use case GetUserInvitation."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.get_user_invitation import (
    GetUserInvitationCommand,
    GetUserInvitation,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Fixture for creating the invitation repository."""
    return InvitationDbRepository(database)


def test_get_invitation(repo: UserInvitationRepository, create_user_invitation):
    """Test the use case: get user invitation."""
    user_invitation = create_user_invitation()

    command = GetUserInvitationCommand(uuid=str(user_invitation.uuid))
    result = GetUserInvitation(repo).execute(command)

    assert (
        result.uuid == user_invitation.uuid
    ), "The invitation must have the same uuid."
