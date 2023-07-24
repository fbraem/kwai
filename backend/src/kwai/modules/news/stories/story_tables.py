"""Module that defines all dataclasses for the tables containing stories."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.rows import ContentRow
from kwai.core.db.table import Table
from kwai.core.domain.value_objects.content import Content
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.news.stories.story import (
    Application,
    Promotion,
    StoryEntity,
    StoryIdentifier,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class StoryContentRow(ContentRow):
    """Represent a row in the news_contents table.

    Attributes:
        news_id: The id of the news story
    """

    news_id: int

    @classmethod
    def persist(cls, story: StoryEntity, content: Content):
        """Persist a content value object to the table.

        Args:
            story: The story that contains the content.
            content: The content of a story.
        """
        return StoryContentRow(
            news_id=story.id.value,
            locale=content.locale,
            format=content.format,
            title=content.title,
            content=content.content,
            summary=content.summary,
            user_id=content.author.id.value,
            created_at=content.traceable_time.created_at.timestamp,
            updated_at=content.traceable_time.updated_at.timestamp,
        )


StoryContentsTable = Table("news_contents", StoryContentRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class ApplicationRow:
    """Represent the application data that is associated with a story."""

    id: int
    name: str
    title: str

    def create_application(self) -> Application:
        """Create an Application value object from row data."""
        return Application(id=IntIdentifier(self.id), name=self.name, title=self.title)


ApplicationsTable = Table("applications", ApplicationRow)


@dataclass(kw_only=True, frozen=True, slots=True)
class StoryRow:
    """Represent a table row of the stories table.

    Attributes:
        id: the id of the story
        enabled: is the story enabled?
        promotion: the priority to use for the promotion
        promotion_end_date: when ends the promotion?
        publish_date: time of publication
        end_date: end of publication
        remark: a remark about the story
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
        self, application: Application, content: list[Content]
    ) -> StoryEntity:
        """Create a story entity from a table row."""
        return StoryEntity(
            id_=StoryIdentifier(self.id),
            enabled=self.enabled == 1,
            promotion=Promotion(
                priority=self.promotion,
                end_date=LocalTimestamp(self.promotion_end_date),
            ),
            period=Period(
                start_date=LocalTimestamp(self.publish_date),
                end_date=LocalTimestamp(self.end_date),
            ),
            application=application,
            content=content,
            remark=self.remark,
            traceable_time=TraceableTime(
                created_at=LocalTimestamp(timestamp=self.created_at),
                updated_at=LocalTimestamp(timestamp=self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, story: StoryEntity) -> "StoryRow":
        """Persist an entity to row data.

        Args:
            story: The story to persist.
        """
        return StoryRow(
            id=story.id.value,
            enabled=1 if story.is_enabled else 0,
            promotion=story.promotion.priority,
            promotion_end_date=story.promotion.end_date.timestamp,
            publish_date=story.period.start_date.timestamp,
            end_date=None if story.period.endless else story.period.end_date.timestamp,
            remark=story.remark,
            application_id=story.application.id.value,
            created_at=story.traceable_time.created_at.timestamp,
            updated_at=story.traceable_time.updated_at.timestamp,
        )


StoriesTable = Table("news_stories", StoryRow)
