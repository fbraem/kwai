"""Module that defines the Update Team use case."""

from dataclasses import dataclass

from kwai.core.domain.entity import Entity
from kwai.core.domain.presenter import Presenter
from kwai.modules.teams.domain.team import TeamEntity, TeamIdentifier
from kwai.modules.teams.repositories.team_repository import TeamRepository


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateTeamCommand:
    """Input for the Update Team use case."""

    id: int
    name: str
    active: bool
    remark: str


class UpdateTeam:
    """Use case for updating a team."""

    def __init__(self, team_repo: TeamRepository, presenter: Presenter[TeamEntity]):
        """Initialize the use case.

        Args:
            team_repo: A repository for updating the team.
            presenter: A presenter for a team entity.
        """
        self._team_repo = team_repo
        self._presenter = presenter

    async def execute(self, command: UpdateTeamCommand) -> None:
        """Execute the use case.

        Raises:
            TeamNotFoundException: raise when the team does not exist.
        """
        team = await self._team_repo.get(
            self._team_repo.create_query().filter_by_id(TeamIdentifier(command.id))
        )

        team = Entity.replace(
            team,
            name=command.name,
            active=command.active,
            remark=command.remark,
            traceable_time=team.traceable_time.mark_for_update(),
        )
        await self._team_repo.update(team)

        self._presenter.present(team)
