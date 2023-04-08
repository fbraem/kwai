"""Module for testing the use case mail a user invitation."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.mail_user_invitation import (
    MailUserInvitationCommand,
    MailUserInvitation,
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
def repo(database: Database) -> UserInvitationRepository:
    """Create a user invitation repository."""
    return InvitationDbRepository(database)


@pytest.fixture(scope="module")
def user_invitation(
    repo: UserInvitationRepository, user: UserEntity
) -> UserInvitationEntity:
    """Fixture for a user invitation."""
    invitation = UserInvitationEntity(
        email=EmailAddress("ichiro.abe@kwai.com"),
        name=Name(first_name="Ichiro", last_name="Abe"),
        user=user,
    )
    entity = repo.create(invitation)
    yield entity
    repo.delete(entity)


def test_mail_user_invitation(
    repo: UserInvitationRepository,
    user_invitation: UserInvitationEntity,
    mailer: Mailer,
    recipients: Recipients,
    user_invitation_mail_template: MailTemplate,
):
    """Test use case mail user invitation"""
    command = MailUserInvitationCommand(uuid=str(user_invitation.uuid))
    updated_user_invitation = MailUserInvitation(
        repo, mailer, recipients, user_invitation_mail_template
    ).execute(command)

    assert updated_user_invitation.mailed is not None, "mailed should be set."


def test_mail_user_invitation_already_mailed(
    repo: UserInvitationRepository,
    user_invitation: UserInvitationEntity,
    mailer: Mailer,
    recipients: Recipients,
    user_invitation_mail_template: MailTemplate,
):
    """Test when a user invitation is already sent."""
    command = MailUserInvitationCommand(uuid=str(user_invitation.uuid))
    with pytest.raises(UnprocessableException):
        MailUserInvitation(
            repo, mailer, recipients, user_invitation_mail_template
        ).execute(command)
