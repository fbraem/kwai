"""Module that defines common table classes."""

from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import Table
from kwai.core.db.table_row import TableRow
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId


@dataclass(kw_only=True, frozen=True, slots=True)
class OwnerRow:
    """Represent the owner data."""

    id: int
    uuid: str
    first_name: str
    last_name: str

    def create_owner(self) -> Owner:
        """Create an Author value object from row data."""
        return Owner(
            id=IntIdentifier(self.id),
            uuid=UniqueId.create_from_string(self.uuid),
            name=Name(first_name=self.first_name, last_name=self.last_name),
        )


OwnersTable = Table("users", OwnerRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class OwnerTableRow(TableRow):
    """Represent the owner data."""

    __table_name__ = "users"

    id: int
    uuid: str
    first_name: str
    last_name: str

    def create_owner(self) -> Owner:
        """Create an Author value object from row data."""
        return Owner(
            id=IntIdentifier(self.id),
            uuid=UniqueId.create_from_string(self.uuid),
            name=Name(first_name=self.first_name, last_name=self.last_name),
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class TextRow:
    """Represent a row for a content table.

    Attributes:
        locale: The code of the locale of the text
        format: The format of the text (md = markdown, html, ...)
        title: The title of the text
        content: The long content of the text
        summary: A summary of the text
        user_id: The id of the author
        created_at: the timestamp of creation
        updated_at: the timestamp of the last modification
    """

    locale: str
    format: str
    title: str
    content: str
    summary: str
    user_id: int
    created_at: datetime
    updated_at: datetime | None

    def create_text(self, author: Owner) -> LocaleText:
        """Create a LocaleText value object from a row.

        Args:
            author: The author of the text.
        """
        return LocaleText(
            locale=Locale(self.locale),
            format=DocumentFormat(self.format),
            title=self.title,
            content=self.content,
            summary=self.summary,
            author=author,
            traceable_time=TraceableTime(
                created_at=Timestamp(timestamp=self.created_at),
                updated_at=Timestamp(timestamp=self.updated_at),
            ),
        )
