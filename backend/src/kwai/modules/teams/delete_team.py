"""Module that defines the use case "Delete Team"."""

from dataclasses import dataclass

from kwai.modules.teams.domain.team import TeamIdentifier
from kwai.modules.teams.repositories.team_repository import TeamRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class DeleteTeamCommand:
    """Input for the use case DeleteTeam."""

    id: int


class DeleteTeam:
    """Use case for deleting a team."""

    def __init__(self, repo: TeamRepository):
        """Initialize the use case.

        Args:
            repo: A repository for deleting a team.
        """
        self._repo = repo

    async def execute(self, command: DeleteTeamCommand) -> None:
        """Execute the use case.

        Args:
            command: The input for the use case.

        Raises:
            TeamNotFoundException: If the team does not exist.
        """
        team = await self._repo.get(
            self._repo.create_query().filter_by_id(TeamIdentifier(command.id))
        )
        # TODO: check if the team is not attached to one or more trainings...
        await self._repo.delete(team)
