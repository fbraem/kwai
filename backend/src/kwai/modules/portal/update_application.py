"""Module that defines the use case: update an application."""

from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class UpdateApplicationCommand:
    """Input for the use case [UpdateApplication][kwai.modules.portal.update_application.UpdateApplication].

    Attributes:
        id: The id of the application
    """

    id: int
    title: str
    short_description: str
    description: str
    remark: str
    weight: int
    events: bool
    pages: bool
    news: bool


class UpdateApplication:
    """Implements the use case 'update an application'."""

    def __init__(self, application_repo: ApplicationRepository):
        """Initialize the use case.

        Args:
            application_repo: A repository for updating an application.
        """
        self._application_repo = application_repo

    async def execute(self, command: UpdateApplicationCommand) -> ApplicationEntity:
        """Execute the use case.

        Args:
            command: The input for this use case.
        """
        application = await self._application_repo.get_by_id(IntIdentifier(command.id))
        updated_application = Entity.replace(
            application,
            title=command.title,
            short_description=command.short_description,
            description=command.description,
            remark=command.remark,
            events=command.events,
            pages=command.pages,
            news=command.news,
            weight=command.weight,
        )
        await self._application_repo.update(updated_application)
        return updated_application
