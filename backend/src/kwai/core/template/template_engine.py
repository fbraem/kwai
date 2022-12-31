"""Module that defines an interface for a template engine."""
from abc import abstractmethod

from kwai.core.template import Template


class TemplateEngine:
    """Interface for a template engine."""

    @abstractmethod
    def create(self, template_file_path: str, lang: str = "nl") -> Template:
        """Create a template from the given file path."""
        raise NotImplementedError
