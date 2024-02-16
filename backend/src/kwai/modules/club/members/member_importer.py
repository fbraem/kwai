"""Module for defining an abstract class for importing member entities."""
from abc import ABC, abstractmethod
from functools import lru_cache

from typing_extensions import AsyncGenerator

from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.members.country_repository import CountryRepository
from kwai.modules.club.members.file_upload import FileUploadEntity
from kwai.modules.club.members.member import MemberEntity
from kwai.modules.club.members.value_objects import Country


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
    async def import_(self) -> AsyncGenerator[MemberEntity, None]:
        """Import member entities.

        When a member is available, use yield to pass the member entity.
        """

    def create_file_upload_entity(self) -> FileUploadEntity:
        """Create a file upload entity."""
        return FileUploadEntity(filename=self._filename, owner=self._owner)

    @staticmethod
    @lru_cache
    async def _get_country(
        country_repo: CountryRepository, iso_2: str
    ) -> Country | None:
        """Gets the country from the repository.

        The value is cached.

        Note: to avoid memory leaks, this method is a static method.
        """
        return await country_repo.get_by_iso_2(iso_2)
