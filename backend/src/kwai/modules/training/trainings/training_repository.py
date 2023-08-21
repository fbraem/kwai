"""Module that defines an interface for a repository of trainings."""
from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.training.trainings.training import TrainingEntity, TrainingIdentifier
from kwai.modules.training.trainings.training_query import TrainingQuery


class TrainingNotFoundException(Exception):
    """Raised when a training can not be found."""


class TrainingRepository(ABC):
    """An interface for a repository of trainings."""

    @abstractmethod
    def create_query(self) -> TrainingQuery:
        """Create a query for querying trainings."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        query: TrainingQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[TrainingEntity]:
        """Return all trainings of a given query.

        Args:
            query: The query to use for selecting the rows.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Returns:
            A list of trainings.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: TrainingIdentifier) -> TrainingEntity:
        """Get the training with the given id.

        Args:
            id: The id of the training.

        Returns:
            A training entity.
        """
        raise NotImplementedError
