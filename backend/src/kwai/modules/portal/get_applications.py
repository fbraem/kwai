"""Module that defines the use case: get all applications for a portal."""
from dataclasses import dataclass

# pylint: disable=too-few-public-methods


@dataclass(kw_only=True, frozen=True, slots=True)
class GetApplicationsCommand:
    """Input for the use case
    [GetApplications][kwai.modules.portal.get_applications.GetApplication]

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

    def __init__(self):
        pass

    async def execute(self, command: GetApplicationsCommand):
        """Execute the use case.

        Args:
            command: The input for this use case.
        """
