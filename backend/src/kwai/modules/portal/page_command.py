"""Module that defines common command for create/update pages."""
from dataclasses import dataclass

from kwai.core.domain.use_case import TextCommand


@dataclass(kw_only=True, frozen=True, slots=True)
class PageCommand:
    """Input for the use case "Create Page"."""

    enabled: bool
    texts: list[TextCommand]
    application: int
    priority: int
    remark: str
