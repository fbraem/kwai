"""Module for testing mail_user_recovery."""
from datetime import datetime

import pytest

from kwai.core.db import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects import UniqueId, LocalTimestamp, EmailAddress, Name
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.mail_user_recovery import (
    MailUserRecovery,
    MailUserRecoveryCommand,
)
from kwai.modules.identity.user_recoveries import (
    UserRecoveryRepository,
    UserRecoveryDbRepository,
    UserRecoveryEntity,
    UserRecovery,
)
from kwai.modules.identity.users.user import UserEntity, User


@pytest.fixture(scope="module")
def repo(database: Database) -> UserRecoveryRepository:
    return UserRecoveryDbRepository(database)


@pytest.fixture(scope="module")
def user_recovery(repo: UserRecoveryRepository) -> UserRecoveryEntity:
    user_recovery = UserRecovery(
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
    )
    entity = repo.create(user_recovery)
    yield entity
    repo.delete(entity)


def test_mail_user_recovery(
    repo: UserRecoveryRepository,
    user_recovery: UserRecoveryEntity,
    mailer: Mailer,
    recipients: Recipients,
    recovery_mail_template: MailTemplate,
):
    command = MailUserRecoveryCommand(uuid=str(user_recovery.uuid))
    updated_user_recovery = MailUserRecovery(
        repo,
        mailer,
        recipients,
        recovery_mail_template,
    ).execute(command)

    assert updated_user_recovery.mailed is not None, "mailed should be set."


def test_mail_user_recovery_already_mailed(
    repo: UserRecoveryRepository,
    user_recovery: UserRecoveryEntity,
    mailer: Mailer,
    recipients: Recipients,
    recovery_mail_template: MailTemplate,
):
    command = MailUserRecoveryCommand(uuid=str(user_recovery.uuid))
    with pytest.raises(UnprocessableException):
        MailUserRecovery(
            repo,
            mailer,
            recipients,
            recovery_mail_template,
        ).execute(command)
