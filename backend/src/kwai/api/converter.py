from abc import ABC, abstractmethod

import markdown


class DocumentConverter(ABC):
    """Interface for a document converter.

    A converter will convert a certain format (markdown for example) into HTML.
    """

    @abstractmethod
    def convert(self, content: str) -> str:
        """Convert a string to HTML."""
        raise NotImplementedError


class MarkdownConverter(DocumentConverter):
    """Converter for converting markdown into HTML."""

    def convert(self, content: str) -> str:
        """Convert markdown to HTML."""
        return markdown.markdown(content)
