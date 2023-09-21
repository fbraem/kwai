"""Module that defines common command for create/update pages."""
from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class TextCommand:
    """Input for a text."""

    locale: str
    format: str
    title: str
    summary: str
    content: str


@dataclass(kw_only=True, frozen=True, slots=True)
class PageCommand:
    """Input for the use case "Create Page"."""

    enabled: bool
    text: list[TextCommand]
    application: int
    priority: int
    remark: str
