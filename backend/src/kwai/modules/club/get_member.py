"""Module that implements the use case 'Get Member'."""

from dataclasses import dataclass

from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.members.member_repository import MemberRepository


@dataclass(kw_only=True, frozen=True, slots=True)
class GetMemberCommand:
    """The input for the use case 'Get Member'.

    Attributes:
        uuid: The unique id of the member.
    """

    uuid: str


class GetMember:
    """Use case 'Get Member'."""

    def __init__(self, repo: MemberRepository):
        """Initialize the use case.

        Args:
            repo: The repository used to get the member.
        """
        self._repo = repo

    async def execute(self, command: GetMemberCommand) -> MemberEntity:
        """Execute the use case.

        Args:
            command: the input for this use case.

        Returns:
            The member (if it exists) with the given uuid.

        Throws:
            MemberNotFoundException: raised when the member does not exist.
        """
        query = self._repo.create_query()
        query.filter_by_uuid(UniqueId.create_from_string(command.uuid))

        return await self._repo.get(query)
