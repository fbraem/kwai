"""Module for defining all table classes for page."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.rows import ContentRow
from kwai.core.db.table import Table
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.text import LocaleText
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.pages.page import PageEntity, PageIdentifier


@dataclass(kw_only=True, frozen=True, slots=True)
class PageContentRow(ContentRow):
    """Represent a row in the page_contents table.

    Attributes:
        page_id: The id of a page.
    """

    page_id: int

    @classmethod
    def persist(cls, page: PageEntity, content: LocaleText):
        """Persist a content value object to the table.

        Args:
            page: The page that contains the content.
            content: The content of a story.
        """
        return PageContentRow(
            page_id=page.id.value,
            locale=content.locale.value,
            format=content.format.value,
            title=content.title,
            content=content.content,
            summary=content.summary,
            user_id=content.author.id.value,
            created_at=content.traceable_time.created_at.timestamp,
            updated_at=content.traceable_time.updated_at.timestamp,
        )


PageContentsTable = Table("page_contents", PageContentRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class PageRow:
    """Represent a table row of the page table.

    Attributes:
        id: the id of the page.
        enabled: is this page enabled?
        remark: a remark about the page
        application_id: the link to the application
        priority: the priority of the page
        created_at: the timestamp of creation
        updated_at: the timestamp of the last modification
    """

    id: int
    enabled: int
    remark: str | None
    application_id: int
    priority: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(
        self, application: ApplicationEntity, content: list[LocaleText]
    ) -> PageEntity:
        """Create a page entity from a table row."""
        return PageEntity(
            id_=PageIdentifier(id_=self.id),
            enabled=self.enabled == 1,
            application=application,
            priority=self.priority,
            content=content,
            remark=self.remark,
            traceable_time=TraceableTime(
                created_at=LocalTimestamp(timestamp=self.created_at),
                updated_at=LocalTimestamp(timestamp=self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, page: PageEntity) -> "PageRow":
        """Persist an entity to row data.

        Args:
            page: The page to persist.
        """
        return PageRow(
            id=page.id.value,
            enabled=1 if page.enabled else 0,
            remark=page.remark or "",
            application_id=page.application.id.value,
            priority=page.priority,
            created_at=page.traceable_time.created_at.timestamp,
            updated_at=page.traceable_time.updated_at.timestamp,
        )


PagesTable = Table("pages", PageRow)
