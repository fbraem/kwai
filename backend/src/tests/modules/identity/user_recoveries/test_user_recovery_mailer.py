from datetime import datetime

import pytest

from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.user_recoveries.user_recovery_mailer import (
    UserRecoveryMailer,
)
from kwai.modules.identity.users.user import UserEntity


@pytest.fixture(scope="module")
def user_recovery() -> UserRecoveryEntity:
    """Fixture creating a user recovery entity."""
    return UserRecoveryEntity(
        expiration=LocalTimestamp(timestamp=datetime.utcnow(), timezone="UTC"),
        user=UserEntity(
            email=EmailAddress("jigoro.kano@kwai.com"),
            name=Name(first_name="Jigoro", last_name="Kano"),
        ),
    )


def test_user_recovery_mailer_send(
    mailer: Mailer,
    recipients: Recipients,
    recovery_mail_template: MailTemplate,
    user_recovery: UserRecoveryEntity,
):
    """Test user recovery mailer send"""
    mail = UserRecoveryMailer(
        mailer,
        recipients,
        recovery_mail_template,
        user_recovery,
    ).send()

    assert mail, "There should be an email."
