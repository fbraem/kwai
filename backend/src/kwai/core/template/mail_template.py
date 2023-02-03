"""Module that defines a template for creating HTML/Text mails."""
from typing import Any

from kwai.core.mail.mail import Mail
from kwai.core.mail.recipient import Recipients
from .template import Template


class MailTemplate:
    """Defines a wrapper around template to generate an HTML and text mail."""

    def __init__(self, html_template: Template, text_template: Template):
        self._html_template = html_template
        self._text_template = text_template

    def render_html(self, **kwargs: dict[str, Any]) -> str:
        """Render the HTML template."""
        return self._html_template.render(**kwargs)

    def render_text(self, **kwargs: dict[str, Any]) -> str:
        """Render the text template."""
        return self._text_template.render(**kwargs)

    def create_mail(self, recipients: Recipients, subject: str, **kwargs):
        """Create the mail with HTML and text template."""
        return Mail(
            recipients,
            subject,
            self.render_text(**kwargs),
            self.render_html(**kwargs),
        )
