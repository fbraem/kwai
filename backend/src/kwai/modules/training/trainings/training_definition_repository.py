"""Module that defines an interface for a training definition repository."""

from abc import ABC, abstractmethod
from typing import AsyncIterator

from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionEntity,
    TrainingDefinitionIdentifier,
)
from kwai.modules.training.trainings.training_definition_query import (
    TrainingDefinitionQuery,
)


class TrainingDefinitionNotFoundException(Exception):
    """Raised when a training definition can not be found."""


class TrainingDefinitionRepository(ABC):
    """A training definition repository."""

    @abstractmethod
    def create_query(self) -> TrainingDefinitionQuery:
        """Create a query for querying training definitions."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self, id_: TrainingDefinitionIdentifier
    ) -> TrainingDefinitionEntity:
        """Get the training definition with the given id.

        Args:
            id_: The id of the training definition.

        Returns:
            A training definition

        Raises:
            TrainingDefinitionNotFoundException: when the training definition
                cannot be found.
        """

    @abstractmethod
    async def get_all(
        self,
        query: TrainingDefinitionQuery | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> AsyncIterator[TrainingDefinitionEntity]:
        """Return all training definitions of a given query.

        Args:
            query: The query to use for selecting the rows.
            limit: The maximum number of entities to return.
            offset: Skip the offset rows before beginning to return entities.

        Yields:
            A list of applications.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(
        self, training_definition: TrainingDefinitionEntity
    ) -> TrainingDefinitionEntity:
        """Create a new training definition entity.

        Args:
            training_definition: The training definition to create.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, training_definition: TrainingDefinitionEntity):
        """Update an application entity.

        Args:
            training_definition: The training definition to update.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, training_definition: TrainingDefinitionEntity):
        """Delete an application entity.

        Args:
            training_definition: The training definition to delete.
        """
        raise NotImplementedError
