"""Module for the use case "Get Pages"."""
from dataclasses import dataclass

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.modules.page.pages.page_repository import PageRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetPagesCommand:
    """Input for the "Get Pages" use case."""

    offset: int | None = None
    limit: int | None = None
    application: int | str | None = None


class GetPages:
    """Use case "Get Pages"."""

    def __init__(self, repo: PageRepository):
        """Initialize the use case.

        Args:
            repo: A repository to get pages.
        """
        self._repo = repo

    async def execute(self, command: GetPagesCommand) -> UseCaseBrowseResult:
        """Executes the use case."""
        query = self._repo.create_query()

        if command.application is not None:
            query.filter_by_application(command.application)

        return UseCaseBrowseResult(
            await query.count(),
            self._repo.get_all(query, limit=command.limit, offset=command.offset),
        )
