"""Module for defining the use case 'Get Members'."""

from dataclasses import dataclass

from kwai.core.domain.presenter import AsyncPresenter, IterableResult
from kwai.modules.teams.domain.team import TeamIdentifier
from kwai.modules.teams.domain.team_member import MemberEntity
from kwai.modules.teams.repositories.member_repository import MemberRepository


@dataclass(frozen=True, kw_only=True, slots=True)
class GetMembersCommand:
    """Input for the use case 'Get Members'.

    When in_team is False and a team_id is set, only the members that are not
    part of that team will be returned.
    """

    team_id: int | None = None
    in_team: bool = True
    limit: int | None = None
    offset: int | None = None


class GetMembers:
    """Implements the use case 'Get Members'."""

    def __init__(
        self,
        member_repository: MemberRepository,
        presenter: AsyncPresenter[IterableResult[MemberEntity]],
    ):
        """Initialize the use case."""
        self._member_repository = member_repository
        self._presenter = presenter

    async def execute(self, command: GetMembersCommand):
        """Execute the use case."""
        member_query = self._member_repository.create_query()
        if command.team_id is not None:
            member_query = member_query.filter_by_team(
                TeamIdentifier(command.team_id), command.in_team
            )
        await self._presenter.present(
            IterableResult(
                count=await member_query.count(),
                limit=command.limit,
                offset=command.offset,
                iterator=self._member_repository.get_all(member_query),
            )
        )
