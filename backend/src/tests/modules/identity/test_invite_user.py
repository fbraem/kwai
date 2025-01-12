"""Module for testing the use case: invite a user."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.events.publisher import Publisher
from kwai.modules.identity.invite_user import InviteUser, InviteUserCommand
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_db_repository import UserDbRepository

pytestmark = [pytest.mark.db, pytest.mark.bus]


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Create a user invitation repository."""
    return UserInvitationDbRepository(database)


async def test_invite_user(
    database: Database,
    repo: UserInvitationRepository,
    user: UserEntity,
    publisher: Publisher,
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
        user=user, user_repo=user_repo, user_invitation_repo=repo, publisher=publisher
    ).execute(command)

    assert user_invitation is not None, "There should be a user invitation"


async def test_user_already_exists(
    database: Database,
    repo: UserInvitationRepository,
    make_user_account_in_db,
    publisher: Publisher,
):
    """Test if an exception is raised when a user with the email already exists."""
    user_account = await make_user_account_in_db()
    user_repo = UserDbRepository(database)
    command = InviteUserCommand(
        email=str(user_account.user.email),
        first_name="Jigoro",
        last_name="Kano",
        remark="Created with pytest test_user_already_exists",
    )

    with pytest.raises(UnprocessableException):
        await InviteUser(
            user=user_account.user,
            user_repo=user_repo,
            user_invitation_repo=repo,
            publisher=publisher,
        ).execute(command)


async def test_already_invited_user(
    database: Database,
    repo: UserInvitationRepository,
    make_user_account_in_db,
    make_user_invitation_in_db,
    publisher: Publisher,
):
    """Test if an exception is raised when there is an invitation pending."""
    user_account = await make_user_account_in_db()
    # Make already a user invitation
    user_invitation = await make_user_invitation_in_db()

    # Try to make the same user invitation
    user_repo = UserDbRepository(database)
    command = InviteUserCommand(
        email=str(user_invitation.email),
        first_name=user_account.user.name.first_name,
        last_name=user_account.user.name.last_name,
        remark="Created with pytest test_already_invited_user",
    )

    with pytest.raises(UnprocessableException):
        await InviteUser(
            user=user_account.user,
            user_repo=user_repo,
            user_invitation_repo=repo,
            publisher=publisher,
        ).execute(command)
