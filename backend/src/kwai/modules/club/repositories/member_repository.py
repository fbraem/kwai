"""Module that defines an interface for a Member repository."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from kwai.modules.club.domain.file_upload import FileUploadEntity
from kwai.modules.club.domain.member import MemberEntity
from kwai.modules.club.repositories.member_query import MemberQuery


class MemberNotFoundException(Exception):
    """Raised when a Member cannot be found."""


class MemberRepository(ABC):
    """An interface for a repository of members."""

    @abstractmethod
    def create_query(self) -> MemberQuery:
        """Create a query for querying members."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, query: MemberQuery | None = None) -> MemberEntity:
        """Return the first returned element of the given query.

        Args:
            query: The query to use for getting the first member.

        Raises:
            MemberNotFoundException
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        query: MemberQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncGenerator[MemberEntity, None]:
        """Return all members of a given query.

        Args:
            query: The query to use for selecting the members.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A member entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, member: MemberEntity) -> MemberEntity:
        """Create a member.

        Args:
            member: The member to save.

        Returns:
            A member entity with an identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, member: MemberEntity) -> None:
        """Update a member.

        Args:
            member: The member to update.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, member: MemberEntity) -> None:
        """Delete a member.

        Args:
            member: The member to delete.
        """
        raise NotImplementedError

    @abstractmethod
    async def activate_members(self, upload: FileUploadEntity) -> None:
        """Activate all members that have been uploaded."""
        raise NotImplementedError

    @abstractmethod
    async def deactivate_members(self, upload: FileUploadEntity) -> None:
        """Deactivate all members that are not being uploaded."""
        raise NotImplementedError
