"""Module that defines an application entity."""
from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.core.domain.value_objects.traceable_time import TraceableTime

ApplicationIdentifier = IntIdentifier


class ApplicationEntity(Entity[ApplicationIdentifier]):
    """An application entity."""

    def __init__(
        self,
        *,
        id_: ApplicationIdentifier | None = None,
        title: str,
        name: str,
        short_description: str,
        description: str = "",
        remark: str = "",
        news: bool = True,
        pages: bool = True,
        events: bool = True,
        weight: int = 0,
        traceable_time: TraceableTime | None = None,
    ):
        """Constructor.

        Args:
            id_: The id of the application entity
            title: The title of the application
            name: A unique name for the application
            short_description: A short description for the application
            description: A long description for the application
            remark: A remark for the application
            news: Can this application contain news?
            pages: Can this application contain pages?
            events: Can this application contain events?
            weight: A weight, can be used to order applications.
            traceable_time: The creation and modification timestamp of the application.
        """
        super().__init__(id_ or ApplicationIdentifier())
        self._title = title
        self._name = name
        self._short_description = short_description
        self._description = description
        self._remark = remark
        self._news = news
        self._pages = pages
        self._events = events
        self._weight = weight
        self._traceable_time = traceable_time or TraceableTime()

    @property
    def id(self) -> ApplicationIdentifier:
        """Return the id."""
        return self._id

    @property
    def title(self) -> str:
        """Return the title."""
        return self._title

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    @property
    def short_description(self) -> str:
        """Return the short description."""
        return self._short_description

    @property
    def description(self) -> str:
        """Return the description."""
        return self._description

    @property
    def remark(self) -> str:
        """Return the remark."""
        return self._remark

    @property
    def can_contain_news(self) -> bool:
        """Return True when the application can contain news."""
        return self._news

    @property
    def can_contain_pages(self) -> bool:
        """Return True when the application can contain pages."""
        return self._pages

    @property
    def can_contain_events(self) -> bool:
        """Return True when the application can contain events."""
        return self._events

    @property
    def weight(self) -> int:
        """Return the weight."""
        return self._weight

    @property
    def traceable_time(self) -> TraceableTime:
        """Return the creation/modification timestamp of this application."""
        return self._traceable_time
