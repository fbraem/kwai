"""Module for testing the use case GetUserInvitation."""

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.get_user_invitation import (
    GetUserInvitation,
    GetUserInvitationCommand,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Fixture for creating the invitation repository."""
    return UserInvitationDbRepository(database)


async def test_get_invitation(
    repo: UserInvitationRepository, make_user_invitation_in_db
):
    """Test the use case: get user invitation."""
    user_invitation = await make_user_invitation_in_db()
    command = GetUserInvitationCommand(uuid=str(user_invitation.uuid))
    result = await GetUserInvitation(repo).execute(command)

    assert (
        result.uuid == user_invitation.uuid
    ), "The invitation must have the same uuid."
