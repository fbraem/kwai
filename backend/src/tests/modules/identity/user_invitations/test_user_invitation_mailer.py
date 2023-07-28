"""Module for testing the user invitation mailer."""
import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_mailer import (
    UserInvitationMailer,
)
from kwai.modules.identity.users.user import UserEntity

pytestmark = pytest.mark.mail


@pytest.fixture(scope="module")
def user_invitation(user: UserEntity) -> UserInvitationEntity:
    """Fixture for a user invitation."""
    return UserInvitationEntity(
        email=EmailAddress("ichiro.abe@kwai.com"),
        name=Name(first_name="Ichiro", last_name="Abe"),
        user=user,
    )


def test_user_recovery_mailer_sent(
    mailer: Mailer,
    recipients: Recipients,
    user_invitation_mail_template: MailTemplate,
    user_invitation: UserInvitationEntity,
):
    """Test user invitation mailer."""
    mail = UserInvitationMailer(
        mailer, recipients, user_invitation_mail_template, user_invitation
    ).send()

    assert mail, "There should be an email."
