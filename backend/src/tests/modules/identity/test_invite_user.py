"""Module for testing the use case: invite a user."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.events.bus import Bus
from kwai.modules.identity.invite_user import InviteUserCommand, InviteUser
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_db_repository import UserDbRepository

pytestmark = pytest.mark.integration
# pylint: disable=redefined-outer-name


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Create a user invitation repository."""
    return UserInvitationDbRepository(database)


@pytest.mark.asyncio
async def test_invite_user(
    database: Database, repo: UserInvitationRepository, user: UserEntity, bus: Bus
):
    """Test use case: invite a user."""
    user_repo = UserDbRepository(database)
    command = InviteUserCommand(
        email="ichiro.abe@kwai.com",
        first_name="Ichiro",
        last_name="Abe",
        remark="Created with pytest test_invite_user",
    )
    user_invitation = await InviteUser(
        user=user, user_repo=user_repo, user_invitation_repo=repo, bus=bus
    ).execute(command)

    assert user_invitation is not None, "There should be a user invitation"


@pytest.mark.asyncio
async def test_user_already_exists(
    database: Database,
    repo: UserInvitationRepository,
    user: UserEntity,
    bus: Bus,
):
    """Test if an exception is raised when a user with the email already exists."""
    user_repo = UserDbRepository(database)
    command = InviteUserCommand(
        email=str(user.email),
        first_name="Jigoro",
        last_name="Kano",
        remark="Created with pytest test_user_already_exists",
    )

    with pytest.raises(UnprocessableException):
        await InviteUser(
            user=user, user_repo=user_repo, user_invitation_repo=repo, bus=bus
        ).execute(command)


@pytest.mark.asyncio
async def test_already_invited_user(
    database: Database, repo: UserInvitationRepository, user: UserEntity, bus: Bus
):
    """Test if an exception is raised when there is an invitation pending."""
    user_repo = UserDbRepository(database)
    command = InviteUserCommand(
        email="ichiro.abe@kwai.com",
        first_name="Ichiro",
        last_name="Abe",
        remark="Created with pytest test_already_invited_user",
    )

    with pytest.raises(UnprocessableException):
        await InviteUser(
            user=user, user_repo=user_repo, user_invitation_repo=repo, bus=bus
        ).execute(command)
