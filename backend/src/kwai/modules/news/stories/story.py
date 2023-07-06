"""Module that defines a story entity."""
from dataclasses import dataclass, field

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.core.domain.value_objects.unique_id import UniqueId

StoryIdentifier = IntIdentifier


@dataclass(frozen=True, kw_only=True, slots=True)
class Promotion:
    """Value object for handling promoted news stories."""

    priority: int = 0
    end_date: LocalTimestamp = field(default_factory=LocalTimestamp)


@dataclass(frozen=True, kw_only=True, slots=True)
class Application:
    """Value object for an application."""

    id: IntIdentifier
    name: str
    title: str


@dataclass(frozen=True, kw_only=True, slots=True)
class Author:
    """Value object for an author of content."""

    id: IntIdentifier
    uuid: UniqueId
    name: Name


@dataclass(frozen=True, kw_only=True, slots=True)
class Content:
    """Value object for the content of a news story."""

    locale: str
    format: str
    title: str
    content: str
    summary: str
    author: Author
    traceable_time: TraceableTime = field(default_factory=TraceableTime)


class StoryEntity(Entity[StoryIdentifier]):
    """A story entity."""

    def __init__(
        self,
        *,
        id_: StoryIdentifier | None = None,
        enabled: bool = False,
        promotion: Promotion = None,
        period: Period = None,
        application: Application,
        content: list[Content],
        remark: str = "",
        traceable_time: TraceableTime | None = None,
    ):
        super().__init__(id_ or StoryIdentifier())
        self._enabled = enabled
        self._promotion = promotion or Promotion()
        self._period = period or Period()
        self._application = application
        self._content = content
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def is_enabled(self) -> bool:
        """Is this story enabled?"""
        return self._enabled

    @property
    def promotion(self) -> Promotion:
        """Return the promotion information of the story."""
        return self._promotion

    @property
    def period(self) -> Period:
        """Return the active period of the story."""
        return self._period

    @property
    def remark(self) -> str:
        """Return the remark."""
        return self._remark

    @property
    def application(self) -> Application:
        """Return the application."""
        return self._application

    @property
    def content(self) -> list[Content]:
        """Return the contents of the story.

        Remark:
            The list is a copy
        """
        return self._content.copy()

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamp of this application."""
        return self._traceable_time
