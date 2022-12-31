"""Module that implements the Template interface for a jinja2 template."""
from typing import Any

import jinja2

from kwai.core.template import Template


class Jinja2Template(Template):
    """A jinja2 template."""

    def __init__(self, template: jinja2.Template, **kwargs):
        """Constructor.

        kwargs will be merged with the variables used in render."""
        self._template = template
        self._variables = kwargs

    def render(self, **kwargs) -> str:
        """Render the template."""
        return self._template.render(kwargs | self._variables)
