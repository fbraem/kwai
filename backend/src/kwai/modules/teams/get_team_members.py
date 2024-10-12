"""Module for defining the use case 'Get Team Members'."""

from dataclasses import dataclass

from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.modules.teams.domain.team import TeamIdentifier
from kwai.modules.teams.domain.team_member import TeamMember
from kwai.modules.teams.repositories.member_repository import MemberRepository


@dataclass(frozen=True, kw_only=True, slots=True)
class GetTeamMembersCommand:
    """Input for the use case 'Get Team Members'."""

    team_id: int | None = None
    in_team: bool = False
    limit: int | None = None
    offset: int | None = None


class GetTeamMembers:
    """Implements the use case 'Get Team Members'.

    Use this use case for getting the members of a team, or to get the members
    that not part of the given team.
    """

    def __init__(
        self,
        member_repository: MemberRepository,
        presenter: AsyncPresenter[IterableResult[TeamMember]],
    ):
        """Initialize the use case."""
        self._member_repository = member_repository
        self._presenter = presenter

    async def execute(self, command: GetTeamMembersCommand):
        """Execute the use case."""
        team_member_query = self._member_repository.create_query()
        team_member_query.filter_by_team(
            TeamIdentifier(command.team_id), command.in_team
        )
        await self._presenter.present(
            IterableResult(
                count=await team_member_query.count(),
                limit=command.limit,
                offset=command.offset,
                iterator=self._member_repository.get_all(team_member_query),
            )
        )
