"""Module that defines fixtures for user recovery testing."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.template.mail_template import MailTemplate
from kwai.core.template.template_engine import TemplateEngine
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.users.user import UserEntity
from tests.fixtures.identity.tokens import *  # noqa
from tests.fixtures.identity.user_invitations import *  # noqa
from tests.fixtures.identity.users import *  # noqa


@pytest.fixture(scope="module")
def recovery_mail_template(template_engine: TemplateEngine) -> MailTemplate:
    """Returns a template for the user recovery mail."""
    return MailTemplate(
        template_engine.create("identity/recover_html"),
        template_engine.create("identity/recover_txt"),
    )


@pytest.fixture(scope="module")
def user_invitation_mail_template(template_engine: TemplateEngine) -> MailTemplate:
    """Returns a template for the user invitation mail."""
    return MailTemplate(
        template_engine.create("identity/invitation_html"),
        template_engine.create("identity/invitation_txt"),
    )


@pytest.fixture
async def user_invitation(database: Database, user: UserEntity) -> UserInvitationEntity:
    """Fixture for a user invitation."""
    repo = UserInvitationDbRepository(database)
    invitation = await repo.create(
        UserInvitationEntity(
            email=EmailAddress("ichiro.abe@kwai.com"),
            name=Name(first_name="Ichiro", last_name="Abe"),
            remark="Created with pytest",
            user=user,
        )
    )
    yield invitation

    await repo.delete(invitation)
