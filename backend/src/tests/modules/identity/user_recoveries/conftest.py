"""Module that defines fixtures for user recovery testing."""
import pytest

from kwai.core.template import TemplateEngine
from kwai.core.template.mail_template import MailTemplate


@pytest.fixture
def mail_template(template_engine: TemplateEngine) -> MailTemplate:
    """Returns a template for the user recovery mail."""
    return MailTemplate(
        template_engine.create("identity/recover_html"),
        template_engine.create("identity/recover_txt"),
    )
