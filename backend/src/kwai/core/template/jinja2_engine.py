"""Modules that implements the template engine interface for jinja2."""

from fastapi.templating import Jinja2Templates
from jinja2 import (
    ChoiceLoader,
    Environment,
    PackageLoader,
    PrefixLoader,
    TemplatesNotFound,
    select_autoescape,
)

from .jinja2_template import Jinja2Template
from .template import Template
from .template_engine import TemplateEngine, TemplateNotFoundException

JINJA2_FILE_EXTENSION = ".jinja2"


class Jinja2Engine(TemplateEngine):
    """Implements the TemplateEngine interface for Jinja2."""

    def __init__(self, **kwargs):
        """Construct a Jinja2Engine.

        kwargs will be merged to the variables that are used to render a template.
        Use it for variables that are used in all templates.
        """
        self._env = Environment(
            loader=ChoiceLoader(
                [
                    PrefixLoader(
                        {
                            "nl": PackageLoader("kwai", "templates"),
                            "en": PackageLoader("kwai", "templates"),
                        }
                    ),
                    PackageLoader("kwai", "templates/nl"),
                    PackageLoader("kwai", "templates"),
                ],
            ),
            autoescape=select_autoescape(
                disabled_extensions=("txt",),
                default_for_string=True,
                default=True,
            ),
            extensions=["jinja2.ext.do"],
        )
        self._variables = kwargs

    @property
    def web_templates(self) -> Jinja2Templates:
        """Return templates that can be used with a TemplateResponse."""
        return Jinja2Templates(env=self._env)

    def create(self, template_file_path: str) -> Template:
        """Create a jinja2 template."""
        try:
            template = self._env.get_template(template_file_path + ".jinja2")
        except TemplatesNotFound as exc:
            raise TemplateNotFoundException(
                f"Could not find a template with name '{template_file_path}'"
            ) from exc

        return Jinja2Template(template, **self._variables)
