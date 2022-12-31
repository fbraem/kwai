"""Module that defines an interface for a template."""
from abc import abstractmethod


class Template:
    """Interface for a template."""

    @abstractmethod
    def render(self, **kwargs):
        """Render the template with the variables."""
        raise NotImplementedError
