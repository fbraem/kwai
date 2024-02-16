"""Module that defines an interface for a Member query."""
from abc import ABC, abstractmethod
from typing import Self

from kwai.core.domain.repository.query import Query
from kwai.modules.club.members.member import MemberIdentifier


class MemberQuery(Query, ABC):
    """An interface for a member query."""

    @abstractmethod
    def filter_by_id(self, id_: MemberIdentifier) -> Self:
        """Filter on the license of the member."""

    @abstractmethod
    def filter_by_license(self, license: str) -> Self:
        """Filter on the license of the member."""
