"""Module for defining factory fixtures for user invitations."""

import pytest

from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account import UserAccountEntity


@pytest.fixture
def make_user_invitation(make_user):
    """Factory fixture for creating a user invitation."""

    def _make_user_invitation(
        email: EmailAddress | None = None,
        name: Name | None = None,
        user: UserEntity | None = None,
        revoked: bool = False,
    ) -> UserInvitationEntity:
        return UserInvitationEntity(
            email=email or EmailAddress("ichiro.abe@kwai.com"),
            name=name or Name(first_name="Ichiro", last_name="Abe"),
            user=user or make_user(),
            revoked=revoked,
        )

    return _make_user_invitation


@pytest.fixture
def make_user_invitation_in_db(
    request, event_loop, database, make_user_invitation, make_user_account_in_db
):
    """Factory fixture for creating a user invitation in the database."""

    async def _make_user_invitation_in_db(
        user_invitation: UserInvitationEntity | None = None,
        user_account: UserAccountEntity | None = None,
    ) -> UserInvitationEntity:
        if user_account is None:
            user_account = await make_user_account_in_db()
        user_invitation = user_invitation or make_user_invitation(
            user=user_account.user
        )
        repo = UserInvitationDbRepository(database=database)

        async with UnitOfWork(database):
            user_invitation = await repo.create(user_invitation)

        def cleanup():
            async def acleanup():
                async with UnitOfWork(database):
                    await repo.delete(user_invitation)

            event_loop.run_until_complete(acleanup())

        request.addfinalizer(cleanup)

        return user_invitation

    return _make_user_invitation_in_db
