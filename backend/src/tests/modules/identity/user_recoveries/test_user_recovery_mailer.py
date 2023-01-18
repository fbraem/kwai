from datetime import datetime

import pytest

from kwai.core.domain.value_objects import UniqueId, LocalTimestamp, EmailAddress, Name
from kwai.core.mail import Recipients, Mailer
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.user_recoveries import UserRecovery, UserRecoveryEntity
from kwai.modules.identity.user_recoveries.user_recovery_mailer import (
    UserRecoveryMailer,
)
from kwai.modules.identity.users import UserEntity, User


@pytest.fixture(scope="module")
def user_recovery() -> UserRecoveryEntity:
    """Fixture creating a user recovery entity."""
    return UserRecoveryEntity(
        id=1,
        domain=UserRecovery(
            uuid=UniqueId.generate(),
            expiration=LocalTimestamp(timestamp=datetime.utcnow(), timezone="UTC"),
            user=UserEntity(
                id=1,
                domain=User(
                    uuid=UniqueId.generate(),
                    email=EmailAddress("jigoro.kano@kwai.com"),
                    name=Name(first_name="Jigoro", last_name="Kano"),
                ),
            ),
        ),
    )


def test_user_recovery_mailer_send(
    mailer: Mailer,
    recipients: Recipients,
    mail_template: MailTemplate,
    user_recovery: UserRecoveryEntity,
):
    """Test user recovery mailer send"""
    mail = UserRecoveryMailer(
        mailer,
        recipients,
        mail_template,
        user_recovery,
    ).send()

    assert mail, "There should be an email."
