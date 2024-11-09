"""Module that defines all dataclasses for the tables containing stories."""

from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.rows import TextRow
from kwai.core.db.table import Table
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import LocaleText
from kwai.core.domain.value_objects.timestamp import Timestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.news.news_item import (
    NewsItemEntity,
    NewsItemIdentifier,
    Promotion,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class NewsItemTextRow(TextRow):
    """Represent a row in the news_contents table.

    Attributes:
        news_id: The id of the news item
    """

    news_id: int

    @classmethod
    def persist(cls, news_item: NewsItemEntity, text: LocaleText):
        """Persist a content value object to the table.

        Args:
            news_item: The news item that contains the content.
            text: The text of a news item.
        """
        return NewsItemTextRow(
            news_id=news_item.id.value,
            locale=text.locale.value,
            format=text.format.value,
            title=text.title,
            content=text.content,
            summary=text.summary,
            user_id=text.author.id.value,
            created_at=text.traceable_time.created_at.timestamp,
            updated_at=text.traceable_time.updated_at.timestamp,
        )


NewsItemTextsTable = Table("news_contents", NewsItemTextRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class NewsItemRow:
    """Represent a table row of the news items table.

    Attributes:
        id: the id of the news item
        enabled: is the news item enabled?
        promotion: the priority to use for the promotion
        promotion_end_date: when ends the promotion?
        publish_date: time of publication
        end_date: end of publication
        remark: a remark about the news item
        application_id: the link to the application
        created_at: the timestamp of creation
        updated_at: the timestamp of the last modification
    """

    id: int
    enabled: int
    promotion: int
    promotion_end_date: datetime | None
    publish_date: datetime
    end_date: datetime | None
    remark: str | None
    application_id: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(
        self, application: ApplicationEntity, texts: list[LocaleText]
    ) -> NewsItemEntity:
        """Create a news item entity from a table row."""
        return NewsItemEntity(
            id_=NewsItemIdentifier(self.id),
            enabled=self.enabled == 1,
            promotion=Promotion(
                priority=self.promotion,
                end_date=Timestamp.create_utc(self.promotion_end_date),
            ),
            period=Period(
                start_date=Timestamp.create_utc(self.publish_date),
                end_date=Timestamp.create_utc(self.end_date),
            ),
            application=application,
            texts=texts,
            remark=self.remark or "",
            traceable_time=TraceableTime(
                created_at=Timestamp.create_utc(timestamp=self.created_at),
                updated_at=Timestamp.create_utc(timestamp=self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, news_item: NewsItemEntity) -> "NewsItemRow":
        """Persist an entity to row data.

        Args:
            news_item: The news item entity to persist.
        """
        return NewsItemRow(
            id=news_item.id.value,
            enabled=1 if news_item.is_enabled else 0,
            promotion=news_item.promotion.priority,
            promotion_end_date=news_item.promotion.end_date.timestamp,
            publish_date=news_item.period.start_date.timestamp,
            end_date=(
                None
                if news_item.period.endless
                else news_item.period.end_date.timestamp
            ),
            remark=news_item.remark,
            application_id=news_item.application.id.value,
            created_at=news_item.traceable_time.created_at.timestamp,
            updated_at=news_item.traceable_time.updated_at.timestamp,
        )


NewsItemsTable = Table("news_stories", NewsItemRow)
