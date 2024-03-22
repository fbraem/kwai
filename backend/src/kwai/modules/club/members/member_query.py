"""Module that defines an interface for a Member query."""

from abc import ABC, abstractmethod
from typing import Self

from kwai.core.domain.repository.query import Query
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.modules.club.members.member import MemberIdentifier


class MemberQuery(Query, ABC):
    """An interface for a member query."""

    @abstractmethod
    def filter_by_id(self, id_: MemberIdentifier) -> Self:
        """Filter on the license of the member."""

    @abstractmethod
    def filter_by_license(self, license: str) -> Self:
        """Filter on the license of the member."""

    @abstractmethod
    def filter_by_license_date(
        self, license_end_month: int, license_end_year: int
    ) -> Self:
        """Filter on the license expiration date."""

    @abstractmethod
    def filter_by_active(self) -> Self:
        """Filter on the active members."""

    @abstractmethod
    def filter_by_uuid(self, uuid: UniqueId) -> Self:
        """Filter on the uuid."""
