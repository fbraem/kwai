"""Module for testing the use case 'Accept User Invitation'."""

import pytest

from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.presenter import Presenter
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.modules.identity.accept_user_invitation import (
    AcceptUserInvitation,
    AcceptUserInvitationCommand,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.users.user_account import UserAccountEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


pytestmark = [pytest.mark.db]


class DummyPresenter(Presenter[UserAccountEntity]):
    """A dummy presenter for testing AcceptUserInvitation."""

    def __init__(self):
        self._entity = None

    def present(self, use_case_result: UserAccountEntity) -> None:
        self._entity = use_case_result

    @property
    def entity(self) -> UserAccountEntity:
        """Return the entity returned by the use case."""
        return self._entity


async def test_accept_user_invitation(
    database: Database,
    make_user_account_in_db,
    make_user_invitation,
    make_user_invitation_in_db,
):
    """Test accepting a user invitation."""
    user = await make_user_account_in_db()
    user_invitation = await make_user_invitation_in_db(
        user_invitation=make_user_invitation(
            email=EmailAddress(email="anton.geesink@kwai.com"),
            name=Name(first_name="Anton", last_name="Geesink"),
            user=user,
        )
    )

    presenter = DummyPresenter()
    command = AcceptUserInvitationCommand(
        uuid=str(user_invitation.uuid),
        first_name=user_invitation.name.first_name,
        last_name=user_invitation.name.last_name,
        remark="Created with test_accept_user_invitation",
        password="Test1234",
    )

    user_account_repo = UserAccountDbRepository(database)

    async with UnitOfWork(database):
        await AcceptUserInvitation(
            UserInvitationDbRepository(database),
            user_account_repo,
            presenter,
        ).execute(command)

    assert presenter.entity, "There should be a new user account"

    async with UnitOfWork(database):
        await user_account_repo.delete(presenter.entity)


async def test_dont_accept_revoked_user_invitation(
    database: Database,
    make_user_account_in_db,
    make_user_invitation,
    make_user_invitation_in_db,
):
    """Test if accepting a revoked user invitation results in an exception."""
    user = await make_user_account_in_db()
    user_invitation = await make_user_invitation_in_db(
        user_invitation=make_user_invitation(
            email=EmailAddress(email="anton.geesink@kwai.com"),
            name=Name(first_name="Anton", last_name="Geesink"),
            user=user,
            revoked=True,
        )
    )

    presenter = DummyPresenter()
    command = AcceptUserInvitationCommand(
        uuid=str(user_invitation.uuid),
        first_name=user_invitation.name.first_name,
        last_name=user_invitation.name.last_name,
        remark="Created with test_dont_accept_revoked_user_invitation",
        password="Test1234",
    )

    user_account_repo = UserAccountDbRepository(database)

    with pytest.raises(
        UnprocessableException,
        match=f"The user invitation with id {user_invitation.uuid} is revoked.",
    ):
        await AcceptUserInvitation(
            UserInvitationDbRepository(database),
            user_account_repo,
            presenter,
        ).execute(command)


async def test_dont_accept_expired_user_invitation(
    database: Database,
    make_user_account_in_db,
    make_user_invitation,
    make_user_invitation_in_db,
):
    """Test if accepting an expired user invitation results in an exception."""
    user = await make_user_account_in_db()
    user_invitation = await make_user_invitation_in_db(
        user_invitation=make_user_invitation(
            email=EmailAddress(email="anton.geesink@kwai.com"),
            name=Name(first_name="Anton", last_name="Geesink"),
            user=user,
            expired_at=Timestamp.create_with_delta(days=-1),
        )
    )

    presenter = DummyPresenter()
    command = AcceptUserInvitationCommand(
        uuid=str(user_invitation.uuid),
        first_name=user_invitation.name.first_name,
        last_name=user_invitation.name.last_name,
        remark="Created with test_dont_accept_expired_user_invitation",
        password="Test1234",
    )

    user_account_repo = UserAccountDbRepository(database)

    with pytest.raises(
        UnprocessableException,
        match=f"The user invitation with id {user_invitation.uuid} is expired.",
    ):
        await AcceptUserInvitation(
            UserInvitationDbRepository(database),
            user_account_repo,
            presenter,
        ).execute(command)


async def test_dont_accept_already_accepted_user_invitation(
    database: Database,
    make_user_account_in_db,
    make_user_invitation,
    make_user_invitation_in_db,
):
    """Test if accepting an already accepted user invitation results in an exception."""
    user = await make_user_account_in_db()
    user_invitation = await make_user_invitation_in_db(
        user_invitation=make_user_invitation(
            email=EmailAddress(email="anton.geesink@kwai.com"),
            name=Name(first_name="Anton", last_name="Geesink"),
            user=user,
            confirmed_at=Timestamp.create_now(),
        )
    )

    presenter = DummyPresenter()
    command = AcceptUserInvitationCommand(
        uuid=str(user_invitation.uuid),
        first_name=user_invitation.name.first_name,
        last_name=user_invitation.name.last_name,
        remark="Created with test_dont_accept_already_accepted_user_invitation",
        password="Test1234",
    )

    user_account_repo = UserAccountDbRepository(database)

    with pytest.raises(
        UnprocessableException,
        match=f"The user invitation with id {user_invitation.uuid} was already accepted.",
    ):
        await AcceptUserInvitation(
            UserInvitationDbRepository(database),
            user_account_repo,
            presenter,
        ).execute(command)


async def test_dont_accept_user_invitation_with_used_email(
    database: Database,
    make_user,
    make_user_account,
    make_user_account_in_db,
    make_user_invitation,
    make_user_invitation_in_db,
):
    """Test if accepting a user invitation with an already used email fails."""
    user = await make_user_account_in_db(
        user_account=make_user_account(
            user=make_user(email=EmailAddress(email="anton.geesink@kwai.com"))
        )
    )
    user_invitation = await make_user_invitation_in_db(
        user_invitation=make_user_invitation(
            email=EmailAddress(email="anton.geesink@kwai.com"),
            name=Name(first_name="Anton", last_name="Geesink"),
            user=user,
        )
    )

    presenter = DummyPresenter()
    command = AcceptUserInvitationCommand(
        uuid=str(user_invitation.uuid),
        first_name=user_invitation.name.first_name,
        last_name=user_invitation.name.last_name,
        remark="Created with test_dont_accept_user_invitation_with_used_email",
        password="Test1234",
    )

    user_account_repo = UserAccountDbRepository(database)

    with pytest.raises(
        UnprocessableException,
        match=f"A user with email {user_invitation.email} already exists.",
    ):
        await AcceptUserInvitation(
            UserInvitationDbRepository(database),
            user_account_repo,
            presenter,
        ).execute(command)
