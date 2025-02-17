"""Module for defining a presenter."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator


@dataclass(frozen=True, kw_only=True, slots=True)
class IterableResult[T]:
    """A dataclass used to represent a result with multiple entities."""

    count: int
    offset: int = 0
    limit: int = 0
    iterator: AsyncIterator[T]


class Presenter[T](ABC):
    """An interface for a presenter.

    A presenter is used to transform an entity into another object that can be used
    in a view.

    An example: convert to a JSON:API resource for returning the entity in a restful
    API.
    """

    @abstractmethod
    def present(self, use_case_result: T) -> None:
        """Present the entity.

        This method is responsible for converting the entity.
        """


class AsyncPresenter[T](ABC):
    """An interface for an async presenter.

    A presenter is used to transform an entity into another object that can be used
    in a view.

    An example: convert to a JSON:API resource for returning the entity in a restful
    API.
    """

    @abstractmethod
    async def present(self, use_case_result: T) -> None:
        """Present the entity.

        This method is responsible for converting the entity.
        """
