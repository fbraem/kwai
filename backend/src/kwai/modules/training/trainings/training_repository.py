"""Module that defines an interface for a repository of trainings."""

from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.training.trainings.training import TrainingEntity, TrainingIdentifier
from kwai.modules.training.trainings.training_definition import TrainingDefinitionEntity
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
    def get_all(
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

    @abstractmethod
    async def create(self, training: TrainingEntity) -> TrainingEntity:
        """Save a training.

        Args:
            training: The training to save.

        Returns:
            A training entity with an identifier.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, training: TrainingEntity) -> None:
        """Update a training.

        Args:
            training: The training to save.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, training: TrainingEntity) -> None:
        """Delete a training.

        Args:
            training: The training to delete.
        """
        raise NotImplementedError

    @abstractmethod
    async def reset_definition(
        self, training_definition: TrainingDefinitionEntity, delete: bool = False
    ) -> None:
        """Reset all trainings of a training definition.

        Args:
            training_definition: The definition to use.
            delete: Delete training or update?

        When delete is True, trainings will be deleted. When False
        the definition will be set to None.
        """
        raise NotImplementedError
