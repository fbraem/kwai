"""Module that defines all dataclasses for the tables containing applications."""
from dataclasses import dataclass
from datetime import datetime

from kwai.core.db.table import Table
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.traceable_time import TraceableTime
from kwai.modules.portal.applications.application import (
    ApplicationEntity,
    ApplicationIdentifier,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class ApplicationRow:
    """Represent a table row of the applications table.

    Attributes:
        id: the id of the application
        title: the title of the application
        name: a unique name for the application
        short_description: a short description about the application
        description: a description about the application
        remark: a remark about the application
        news: does this application can contain news stories?
        pages: does this application can contain pages?
        events does this application can contain events?
        weight: a weight that can be used to order the applications
        created_at: the timestamp of creation
        updated_at: the timestamp of the last modification
    """

    id: int
    title: str
    name: str
    short_description: str
    description: str | None
    remark: str | None
    news: int
    pages: int
    events: int
    weight: int
    created_at: datetime
    updated_at: datetime | None

    def create_entity(self) -> ApplicationEntity:
        return ApplicationEntity(
            id_=ApplicationIdentifier(self.id),
            title=self.title,
            name=self.name,
            short_description=self.description,
            description=self.description or "",
            remark=self.remark or "",
            news=self.news == 1,
            pages=self.pages == 1,
            events=self.events == 1,
            weight=self.weight,
            traceable_time=TraceableTime(
                created_at=LocalTimestamp(self.created_at),
                updated_at=LocalTimestamp(self.updated_at),
            ),
        )

    @classmethod
    def persist(cls, application: ApplicationEntity) -> "ApplicationRow":
        return ApplicationRow(
            id=application.id.value,
            title=application.title,
            name=application.name,
            short_description=application.short_description,
            description=application.description,
            remark=application.remark,
            news=1 if application.can_contain_news else 0,
            pages=1 if application.can_contain_pages else 0,
            events=1 if application.can_contain_events else 0,
            weight=application.weight,
            created_at=application.traceable_time.created_at.timestamp,
            updated_at=application.traceable_time.updated_at.timestamp,
        )


ApplicationsTable = Table("applications", ApplicationRow)
