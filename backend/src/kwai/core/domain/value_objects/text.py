"""Module that defines a value object for text content."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Self

from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.traceable_time import TraceableTime


class Locale(Enum):
    """Value object for a Locale."""

    NL = "nl"
    EN = "en"


class DocumentFormat(Enum):
    """Value object for a document format."""

    HTML = "html"
    MARKDOWN = "md"


@dataclass(frozen=True, kw_only=True, slots=True)
class LocaleText:
    """Value object for text.

    Several entities, like news stories, trainings, contain text. This value object
    represents a text for a certain locale.

    Attributes:
        locale: The locale of the content.
        format: The format of the content.
        title: The title of the content.
        content: The long text of the content.
        summary: The summary of the content.
        author: The author of the content.
        traceable_time: The creation and modification timestamp of the content.
    """

    locale: Locale
    format: DocumentFormat
    title: str
    content: str
    summary: str
    author: Owner
    traceable_time: TraceableTime = field(default_factory=TraceableTime)


class Text:
    """A value object containing content in several locales.

    This class is immutable. A new Text instance will be created and returned when
    content is added, changed or removed.
    """

    def __init__(self, content: dict[Locale, LocaleText] = None):
        """Initialize the text value object with content.

        Args:
            content: A dictionary with content and locale as key.
        """
        self._content = {} if content is None else content.copy()

    def contains_translation(self, locale: Locale) -> bool:
        """Check if the given locale is available as translation.

        Returns:
            True when the translation is available.
        """
        return locale in self._content

    def get_translation(self, locale: Locale) -> LocaleText:
        """Get a translation.

        Args:
            locale: The locale of the content

        Returns:
            The content, when available.

        Raises:
            KeyError: when the locale is not available.
        """
        if locale in self._content:
            return self._content[locale]
        raise KeyError(f"{locale} is not found.")

    def add_translation(self, content: LocaleText) -> "Text":
        """Add a new translation.

        Args:
            content: The translated content.

        Returns:
            A new Text value object that also contains the translated content.

        Raises:
            KeyError: when a translation already existed.
        """
        if content.locale not in self._content:
            return Text(self._content | {content.locale: content})

        raise KeyError(f"{content.locale} was already used.")

    def remove_translation(self, content: LocaleText) -> "Text":
        """Remove a translation.

        Args:
            content: The content to remove.

        Returns:
            A new Text value object that also contains the rest of the translated
            content.

        Raises:
            KeyError: when the translation does not exist.
        """
        if content.locale not in self._content:
            raise KeyError(f"{content.locale} is not found.")
        new_dict = self._content.copy()
        new_dict.pop(content.locale)
        return Text(new_dict)

    def replace_translation(self, content: LocaleText) -> Self:
        """Replace a translation.

        Args:
            content: The content to remove.

        Returns:
            A new Text value object that also contains the rest of the translated
            content.

        Raises:
            KeyError: when the translation does not exist.

        """
        if content.locale not in self._content:
            raise KeyError(f"{content.locale} is not found.")
        return Text(self._content | {content.locale: content})
