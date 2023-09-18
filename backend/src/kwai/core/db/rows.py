"""Module that defines common table classes."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import Table
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.owner import Owner
from kwai.core.domain.value_objects.text import DocumentFormat, Locale, LocaleText
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
class ContentRow:
    """Represent a row for a content table.

    Attributes:
        locale: The code of the locale of the text
        format: The format of the text (md = markdown, html, ...)
        title: The title of the news story
        content: The long content of the news story
        summary: A summary of the content
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

    def create_content(self, author: Owner) -> LocaleText:
        """Create a Content value object from a row.

        Args:
            author: The author of the content.
        """
        return LocaleText(
            locale=Locale(self.locale),
            format=DocumentFormat(self.format),
            title=self.title,
            content=self.content,
            summary=self.summary,
            author=author,
            traceable_time=TraceableTime(
                created_at=LocalTimestamp(timestamp=self.created_at),
                updated_at=LocalTimestamp(timestamp=self.updated_at),
            ),
        )
