"""Module for defining an abstract class for importing member entities."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncGenerator

from async_lru import alru_cache

from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.members.country_repository import CountryRepository
from kwai.modules.club.members.file_upload import FileUploadEntity
from kwai.modules.club.members.member import MemberEntity
from kwai.modules.club.members.value_objects import Country


@dataclass(kw_only=True, frozen=True, slots=True)
class Result:
    """Base dataclass for a result of a member import."""

    row: int


@dataclass(kw_only=True, frozen=True, slots=True)
class OkResult(Result):
    """Dataclass for a successful member import."""

    member: MemberEntity


@dataclass(kw_only=True, frozen=True, slots=True)
class FailureResult(Result):
    """Dataclass for a failed member import."""

    message: str


class MemberImporter(ABC):
    """Abstract class for importing member entities from a file."""

    def __init__(self, filename: str, owner: Owner, country_repo: CountryRepository):
        """Initialize the importer.

        Args:
            filename: The name of the csv file.
            owner: The user that started the upload.
            country_repo: A repository to get the nationality of a member.
        """
        self._filename = filename
        self._owner = owner
        self._country_repo = country_repo

    @abstractmethod
    def import_(self) -> AsyncGenerator[Result, None]:
        """Import member entities.

        For each imported (or failed import) of a member, a result will be yielded.
        """

    def create_file_upload_entity(self) -> FileUploadEntity:
        """Create a file upload entity."""
        return FileUploadEntity(filename=self._filename, owner=self._owner)

    @staticmethod
    @alru_cache
    async def _get_country(
        country_repo: CountryRepository, iso_2: str
    ) -> Country | None:
        """Gets the country from the repository.

        The value is cached.

        Note: to avoid memory leaks, this method is a static method.
        """
        return await country_repo.get_by_iso_2(iso_2)
