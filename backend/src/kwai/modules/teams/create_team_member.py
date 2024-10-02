"""Module that defines the use case for creating a team member."""

from dataclasses import dataclass

from kwai.core.domain.presenter import Presenter
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.teams.domain.team import TeamEntity, TeamIdentifier
from kwai.modules.teams.domain.team_member import TeamMember
from kwai.modules.teams.repositories.member_repository import MemberRepository
from kwai.modules.teams.repositories.team_repository import TeamRepository


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateTeamMemberCommand:
    """Input for the 'Create Team Member' use case."""

    team_id: int
    member_id: str
    active: bool = True


class CreateTeamMember:
    """Implements the 'Create Team Member' use case."""

    def __init__(
        self,
        team_repository: TeamRepository,
        member_repository: MemberRepository,
        presenter: Presenter[TeamEntity],
    ):
        """Initialize the use case.

        Args:
            team_repository: A repository for retrieving the team.
            member_repository: A repository for retrieving the member.
            presenter: A Presenter for processing the result.
        """
        self._team_repository = team_repository
        self._member_repository = member_repository
        self._presenter = presenter

    async def execute(self, command: CreateTeamMemberCommand) -> None:
        """Execute the use case.

        Raises:
            TeamNotFoundException: If the team does not exist.
            MemberNotFoundException: If the member does not exist.
            TeamMemberAlreadyExistException: If the member is already part of the team.
        """
        team_query = self._team_repository.create_query().filter_by_id(
            TeamIdentifier(command.team_id)
        )
        team = await self._team_repository.get(team_query)

        member_query = self._member_repository.create_query().filter_by_uuid(
            UniqueId.create_from_string(command.member_id)
        )
        member = await self._member_repository.get(member_query)

        team_member = TeamMember(member=member, active=command.active)
        team.add_member(team_member)

        await self._team_repository.add_team_member(team, team_member)

        self._presenter.present(team)
