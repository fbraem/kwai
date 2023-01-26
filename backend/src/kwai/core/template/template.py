"""Module that defines an interface for a template."""
from abc import abstractmethod
from typing import Any


class Template:
    """Interface for a template."""

    @abstractmethod
    def render(self, **kwargs: dict[str, Any]) -> str:
        """Render the template with the variables."""
        raise NotImplementedError
