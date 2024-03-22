"""Module that defines the use case 'Get Members'."""

from dataclasses import dataclass

from kwai.core.domain.use_case import UseCaseBrowseResult
from kwai.core.domain.value_objects.date import Date
from kwai.modules.club.members.member_repository import MemberRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetMembersCommand:
    """Input for the get members use case.

    Attributes:
        limit: the max. number of elements to return. Default is None, which means all.
        offset: Offset to use. Default is None.
        active: When true (the default), only return the active members.
        license_end_month: Only return members with a license ending in the given month.
        license_end_year: Only return members with a license ending in the given year.
    """

    limit: int | None = None
    offset: int | None = None
    active: bool = True
    license_end_month: int = 0
    license_end_year: int = 0


class GetMembers:
    """Use case get members."""

    def __init__(self, repo: MemberRepository):
        """Initialize use case.

        Args:
            repo: The repository for members.
        """
        self._repo = repo

    async def execute(self, command: GetMembersCommand) -> UseCaseBrowseResult:
        """Execute the use case.

        Args:
            command: the input for this use case.
        """
        query = self._repo.create_query()

        if command.active:
            query = query.filter_by_active()

        if command.license_end_month != 0:
            query = query.filter_by_license_date(
                command.license_end_month, command.license_end_year or Date.today().year
            )

        return UseCaseBrowseResult(
            count=await query.count(),
            iterator=self._repo.get_all(query, command.limit, command.offset),
        )
