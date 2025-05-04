"""Module that defines fixtures for user recovery testing."""

import pytest

from kwai.core.template.mail_template import MailTemplate
from kwai.core.template.template_engine import TemplateEngine
from tests.fixtures.identity.tokens import *  # noqa
from tests.fixtures.identity.user_invitations import *  # noqa
from tests.fixtures.identity.user_recoveries import *  # noqa
from tests.fixtures.identity.users import *  # noqa


@pytest.fixture(scope="module")
def recovery_mail_template(template_engine: TemplateEngine) -> MailTemplate:
    """Returns a template for the user recovery mail."""
    return MailTemplate(
        template_engine.create("mail/identity/recover_html"),
        template_engine.create("mail/identity/recover_txt"),
    )


@pytest.fixture(scope="module")
def user_invitation_mail_template(template_engine: TemplateEngine) -> MailTemplate:
    """Returns a template for the user invitation mail."""
    return MailTemplate(
        template_engine.create("mail/identity/invitation_html"),
        template_engine.create("mail/identity/invitation_txt"),
    )
