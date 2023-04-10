"""Module for testing the use case GetUserInvitation."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.get_user_invitation import (
    GetUserInvitationCommand,
    GetUserInvitation,
)
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)
from kwai.modules.identity.users.user import UserEntity


@pytest.fixture(scope="module")
def user_invitation(
    repo: UserInvitationRepository, user: UserEntity
) -> UserInvitationEntity:
    """Fixture for a user invitation."""
    invitation = UserInvitationEntity(
        email=EmailAddress("ichiro.abe@kwai.com"),
        name=Name(first_name="Ichiro", last_name="Abe"),
        remark="Created with pytest",
        user=user,
    )
    yield repo.create(invitation)
    repo.delete(invitation)


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Create a user invitation repository."""
    return InvitationDbRepository(database)


def test_get_invitation(
    repo: UserInvitationRepository, user_invitation: UserInvitationEntity
):
    """Test the use case: get user invitation."""
    command = GetUserInvitationCommand(uuid=str(user_invitation.uuid))
    result = GetUserInvitation(repo).execute(command)

    assert (
        result.uuid == user_invitation.uuid
    ), "The invitation must have the same uuid."
