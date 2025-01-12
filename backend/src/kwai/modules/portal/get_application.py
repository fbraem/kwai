"""Module that defines the use case: get application for a portal."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class GetApplicationCommand:
    """Input for the use case [GetApplication][kwai.modules.portal.get_application.GetApplication].

    Attributes:
        id: The id of the application
    """

    id: int


class GetApplication:
    """Implements the use case 'get application'."""

    def __init__(self, application_repo: ApplicationRepository):
        """Initialize the use case.

        Args:
            application_repo: A repository for getting applications.
        """
        self._application_repo = application_repo

    async def execute(self, command: GetApplicationCommand):
        """Execute the use case.

        Args:
            command: The input for this use case.
        """
        return await self._application_repo.get_by_id(IntIdentifier(command.id))
