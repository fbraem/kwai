"""Module that defines a story entity."""
from dataclasses import dataclass, field

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.period import Period
from kwai.core.domain.value_objects.text import LocaleText
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.portal.applications.application import ApplicationEntity

StoryIdentifier = IntIdentifier


@dataclass(frozen=True, kw_only=True, slots=True)
class Promotion:
    """Value object for handling promoted news stories."""

    priority: int = 0
    end_date: LocalTimestamp = field(default_factory=LocalTimestamp)


class StoryEntity(Entity[StoryIdentifier]):
    """A story entity."""

    def __init__(
        self,
        *,
        id_: StoryIdentifier | None = None,
        enabled: bool = False,
        promotion: Promotion = None,
        period: Period = None,
        application: ApplicationEntity,
        texts: list[LocaleText],
        remark: str = "",
        traceable_time: TraceableTime | None = None,
    ):
        super().__init__(id_ or StoryIdentifier())
        self._enabled = enabled
        self._promotion = promotion or Promotion()
        self._period = period or Period()
        self._application = application
        self._texts = texts
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def is_enabled(self) -> bool:
        """Check if the story is enabled."""
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
    def application(self) -> ApplicationEntity:
        """Return the application."""
        return self._application

    @property
    def texts(self) -> list[LocaleText]:
        """Return the text content of the story.

        Remark:
            The list is a copy
        """
        return self._texts.copy()

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamp of this application."""
        return self._traceable_time
