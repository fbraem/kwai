"""Module that defines fixtures for user recovery testing."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.core.template.mail_template import MailTemplate
from kwai.core.template.template_engine import TemplateEngine
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.users.user import UserEntity


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


@pytest.fixture(scope="module")
def create_user_invitation(request, database: Database, user: UserEntity):
    """A factory fixture for creating a user invitation."""

    def create(delete=True) -> UserInvitationEntity:
        """Create the user invitation and if requested, delete it after testing."""
        repo = InvitationDbRepository(database)
        invitation = repo.create(
            UserInvitationEntity(
                email=EmailAddress("ichiro.abe@kwai.com"),
                name=Name(first_name="Ichiro", last_name="Abe"),
                remark="Created with pytest",
                user=user,
            )
        )

        # In a factory fixture, it's not possible to use yield, so, add a clean-up
        # function.
        def cleanup():
            repo.delete(invitation)

        if invitation is not None and delete:
            request.addfinalizer(cleanup)

        return invitation

    return create
