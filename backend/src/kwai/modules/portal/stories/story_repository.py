"""Module that defines an interface for a story repository."""
from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.portal.stories.story import StoryEntity, StoryIdentifier
from kwai.modules.portal.stories.story_query import StoryQuery


class StoryNotFoundException(Exception):
    """Raised when the story can not be found."""


class StoryRepository(ABC):
    """Interface for a story repository."""

    @abstractmethod
    async def create(self, story: StoryEntity) -> StoryEntity:
        """Create a new story entity.

        Args:
            story: The story to create

        Returns:
            The story entity with an identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, story: StoryEntity):
        """Update a story entity.

        Args:
            story: The story to update.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, story: StoryEntity):
        """Delete a story.

        Args:
            story: The story to delete.
        """
        raise NotImplementedError

    @abstractmethod
    def create_query(self) -> StoryQuery:
        """Create a query for querying stories."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: StoryIdentifier) -> StoryEntity:
        """Get the story with the given id.

        Args:
            id_: The id of the story.

        Returns:
            A story entity.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        query: StoryQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[StoryEntity]:
        """Return all stories of a given query.

        Args:
            query: The query to use for selecting the rows.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A list of stories.
        """
        raise NotImplementedError
