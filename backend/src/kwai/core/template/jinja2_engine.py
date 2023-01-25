"""Modules that implements the template engine interface for jinja2."""
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplatesNotFound

from kwai.core.template import TemplateEngine, Template, TemplateNotFoundException
from kwai.core.template.jinja2_template import Jinja2Template

JINJA2_FILE_EXTENSION = ".jinja2"


class Jinja2Engine(TemplateEngine):
    """Implements the TemplateEngine interface for Jinja2."""

    def __init__(self, template_path: str, **kwargs):
        """Constructor.

        kwargs will be merged to the variables that are used to render a template.
        Use it for variables that are used in all templates.
        """
        self._env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=select_autoescape(
                disabled_extensions=("txt",),
                default_for_string=True,
                default=True,
            ),
        )
        self._variables = kwargs

    def create(self, template_file_path: str, lang: str = "nl") -> Template:
        """Create a jinja2 template."""
        try:
            template = self._env.select_template(
                [
                    template_file_path + "_" + lang + JINJA2_FILE_EXTENSION,
                    template_file_path + JINJA2_FILE_EXTENSION,
                ]
            )
        except TemplatesNotFound as exc:
            raise TemplateNotFoundException(
                f"Could not find a template with name '{template_file_path}'"
            ) from exc

        return Jinja2Template(template, **self._variables)
