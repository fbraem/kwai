"""Module that defines the Page entity."""
from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.text import LocaleText
from kwai.core.domain.value_objects.traceable_time import TraceableTime

PageIdentifier = IntIdentifier


@dataclass(frozen=True, kw_only=True, slots=True)
class Application:
    """Value object for an application."""

    id: IntIdentifier
    name: str
    title: str


class PageEntity(Entity[PageIdentifier]):
    """A page entity."""

    def __init__(
        self,
        *,
        id_: PageIdentifier | None = None,
        enabled: bool = False,
        application: Application,
        content: list[LocaleText],
        priority: int,
        remark: str,
        traceable_time: TraceableTime | None = None,
    ):
        """Initialize a page entity.

        Args:
            id_: The id of the page.
            enabled: Is this page enabled?
            application: The related application.
            content: The text content of the page.
            priority: The priority level of the page.
            remark: A remark about the page.
            traceable_time: The create and update time of the page.
        """
        super().__init__(id_ or PageIdentifier())
        self._enabled = enabled
        self._application = application
        self._content = content
        self._priority = priority
        self._remark = remark
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def enabled(self) -> bool:
        """Return if the page is enabled."""
        return self._enabled

    @property
    def priority(self) -> int:
        """Return the priority of the page."""
        return self._priority

    @property
    def remark(self) -> str:
        """Return the remark."""
        return self._remark

    @property
    def content(self) -> list[LocaleText]:
        """Return the content."""
        return self._content.copy()

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the created_at."""
        return self._traceable_time

    @property
    def application(self) -> Application:
        """Return the application."""
        return self._application