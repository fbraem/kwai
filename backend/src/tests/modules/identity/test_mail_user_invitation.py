"""Module for testing the use case mail a user invitation."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.mail_user_invitation import (
    MailUserInvitation,
    MailUserInvitationCommand,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
)


pytestmark = [pytest.mark.db, pytest.mark.mail]


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Create a user invitation repository."""
    return UserInvitationDbRepository(database)


async def test_mail_user_invitation(
    repo: UserInvitationRepository,
    make_user_invitation_in_db,
    mailer: Mailer,
    recipients: Recipients,
    user_invitation_mail_template: MailTemplate,
):
    """Test use case mail user invitation."""
    user_invitation = await make_user_invitation_in_db()
    command = MailUserInvitationCommand(uuid=str(user_invitation.uuid))
    updated_user_invitation = await MailUserInvitation(
        repo, mailer, recipients, user_invitation_mail_template
    ).execute(command)

    assert updated_user_invitation.mailed is not None, "mailed should be set."


async def test_mail_user_invitation_already_mailed(
    repo: UserInvitationRepository,
    make_user_invitation_in_db,
    mailer: Mailer,
    recipients: Recipients,
    user_invitation_mail_template: MailTemplate,
):
    """Test when a user invitation is already sent."""
    user_invitation = await make_user_invitation_in_db()
    user_invitation = user_invitation.mail_sent()
    await repo.update(user_invitation)

    command = MailUserInvitationCommand(uuid=str(user_invitation.uuid))
    with pytest.raises(UnprocessableException):
        await MailUserInvitation(
            repo, mailer, recipients, user_invitation_mail_template
        ).execute(command)
