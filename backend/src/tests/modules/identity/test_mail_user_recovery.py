"""Module for testing mail_user_recovery."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.mail.mailer import Mailer
from kwai.core.mail.recipient import Recipients
from kwai.core.template.mail_template import MailTemplate
from kwai.modules.identity.mail_user_recovery import (
    MailUserRecovery,
    MailUserRecoveryCommand,
)
from kwai.modules.identity.user_recoveries.user_recovery import UserRecoveryEntity
from kwai.modules.identity.user_recoveries.user_recovery_db_repository import (
    UserRecoveryDbRepository,
)
from kwai.modules.identity.user_recoveries.user_recovery_repository import (
    UserRecoveryRepository,
)
from kwai.modules.identity.users.user import UserEntity

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def repo(database: Database) -> UserRecoveryRepository:
    """Create a user recovery repository."""
    return UserRecoveryDbRepository(database)


@pytest.fixture(scope="module")
def user_recovery(repo: UserRecoveryRepository, user: UserEntity) -> UserRecoveryEntity:
    """Create a user recovery."""
    user_recovery = UserRecoveryEntity(
        expiration=LocalTimestamp.create_with_delta(hours=2),
        user=user,
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
    """Test use case mail user recovery."""
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
    """Test when a user recovery is already mailed."""
    command = MailUserRecoveryCommand(uuid=str(user_recovery.uuid))
    with pytest.raises(UnprocessableException):
        MailUserRecovery(
            repo,
            mailer,
            recipients,
            recovery_mail_template,
        ).execute(command)
