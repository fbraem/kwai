"""Module that defines a use case for getting teams."""

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.modules.training.teams.team_repository import TeamRepository


class GetTeams:
    """Use case for getting teams."""

    def __init__(self, team_repo: TeamRepository):
        """Initialize the use case.

        Args:
            team_repo: The repository for getting the teams.
        """
        self._team_repo = team_repo

    async def execute(self) -> UseCaseBrowseResult:
        """Execute the use case."""
        team_query = self._team_repo.create_query()
        count = await team_query.count()

        return UseCaseBrowseResult(
            count=count,
            iterator=self._team_repo.get_all(),
        )
