"""Module that defines the use case: get all applications for a portal."""
from dataclasses import dataclass

from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)


# pylint: disable=too-few-public-methods


@dataclass(kw_only=True, frozen=True, slots=True)
class GetApplicationsCommand:
    """Input for the use case
    [GetApplications][kwai.modules.portal.get_applications.GetApplications]

    Attributes:
        name: Only return the application with the given name
        news: Only return applications that can contain news
        events: Only return applications that can contain events
        pages: Only return applications that can contain pages
    """

    name: str = ""
    news: bool = False
    events: bool = False
    pages: bool = False


class GetApplications:
    """Implements the use case 'get applications'."""

    def __init__(self, application_repo: ApplicationRepository):
        """Initialize the use case.

        Args:
            application_repo: A repository for getting applications.
        """
        self._application_repo = application_repo

    async def execute(self, command: GetApplicationsCommand):
        """Execute the use case.

        Args:
            command: The input for this use case.
        """
        query = self._application_repo.create_query()
        return await query.count(), self._application_repo.get_all(query)
