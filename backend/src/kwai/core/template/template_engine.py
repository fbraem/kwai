"""Module that defines an interface for a template engine."""
from abc import abstractmethod

from .template import Template


class TemplateNotFoundException(Exception):
    """Raised when a template cannot be found."""


class TemplateEngine:
    """Interface for a template engine."""

    # pylint: disable=too-few-public-methods
    @abstractmethod
    def create(self, template_file_path: str, lang: str = "nl") -> Template:
        """Create a template from the given file path.

        When the template cannot be found, a TemplateNotFoundException should be raised.
        """
        raise NotImplementedError
