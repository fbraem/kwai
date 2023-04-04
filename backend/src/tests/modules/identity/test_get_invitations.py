"""Tests for the user get invitations."""
from types import GeneratorType

import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.get_invitations import GetInvitationsCommand, GetInvitations
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)

pytestmark = pytest.mark.integration
# pylint: disable=redefined-outer-name


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Create a user invitation repository."""
    return InvitationDbRepository(database)


def test_get_invitations(repo: UserInvitationRepository):
    """Test the use case: get invitations."""
    command = GetInvitationsCommand()
    count, invitations = GetInvitations(repo).execute(command)

    assert count >= 0, "Count must be 0 or greater"
    assert isinstance(
        invitations, GeneratorType
    ), "A list of entities should be yielded"
