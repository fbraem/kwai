"""Tests for the user get invitations."""

from types import AsyncGeneratorType

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.get_invitations import GetInvitations, GetInvitationsCommand
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Create a user invitation repository."""
    return UserInvitationDbRepository(database)


async def test_get_invitations(
    repo: UserInvitationRepository, make_user_invitation_in_db
):
    """Test the use case: get invitations."""
    await make_user_invitation_in_db()

    command = GetInvitationsCommand()
    count, invitations = await GetInvitations(repo).execute(command)

    assert count >= 0, "Count must be 0 or greater"
    assert isinstance(invitations, AsyncGeneratorType), (
        "A list of entities should be yielded"
    )
