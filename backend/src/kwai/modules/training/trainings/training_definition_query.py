"""Module that defines an interface for a training definition query."""


from abc import ABC, abstractmethod

from kwai.core.domain.repository.query import Query
from kwai.modules.training.trainings.training_definition import (
    TrainingDefinitionIdentifier,
)


class TrainingDefinitionQuery(Query, ABC):
    """Interface for a training definition query."""

    @abstractmethod
    def filter_by_id(
        self, id_: TrainingDefinitionIdentifier
    ) -> "TrainingDefinitionQuery":
        """Add a filter on the training definition id.

        Args:
            id_: id of a training definition

        Returns:
            TrainingDefinitionQuery:
        """
        raise NotImplementedError

    @abstractmethod
    def filter_by_ids(
        self, *ids: TrainingDefinitionIdentifier
    ) -> "TrainingDefinitionQuery":
        """Add a filter on multiple training definition identifiers.

        Args:
            ids: a variable list of training definition identifiers

        Returns:
            TrainingDefinitionQuery:
        """
        raise NotImplementedError
