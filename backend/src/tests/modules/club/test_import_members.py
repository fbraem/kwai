"""Module for testing the use case Import Members."""

from pathlib import Path

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.presenter import Presenter
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.club.import_members import ImportMembers, ImportMembersCommand
from kwai.modules.club.repositories.country_db_repository import CountryDbRepository
from kwai.modules.club.repositories.file_upload_db_repository import (
    FileUploadDbRepository,
)
from kwai.modules.club.repositories.file_upload_preview_repository import (
    FileUploadPreviewRepository,
)
from kwai.modules.club.repositories.file_upload_repository import (
    DuplicateMemberUploadedException,
)
from kwai.modules.club.repositories.flemish_member_importer import FlemishMemberImporter
from kwai.modules.club.repositories.member_db_repository import MemberDbRepository


class DummyPresenter[MemberImportResult](Presenter):
    """A dummy presenter."""

    def __init__(self):
        super().__init__()
        self._count = 0

    @property
    def count(self):
        """Return the count."""
        return self._count

    def present(self, use_case_result: MemberImportResult) -> None:
        """Process the result of the use case."""
        self._count += 1


async def test_import_members(database: Database, owner: Owner):
    """Test the use case Import Members."""
    filename = (
        Path(__file__).parent / "repositories" / "data" / "flemish_members_test.csv"
    )

    importer = FlemishMemberImporter(
        str(filename), owner, CountryDbRepository(database)
    )

    command = ImportMembersCommand(preview=False)
    presenter = DummyPresenter()
    await ImportMembers(
        importer,
        FileUploadDbRepository(database),
        MemberDbRepository(database),
        presenter,
    ).execute(command)

    assert presenter.count > 0, "There should be a member uploaded."


async def test_import_preview_members(database: Database, owner: Owner):
    """Test the use case Import Members with preview."""
    filename = (
        Path(__file__).parent / "repositories" / "data" / "flemish_members_test.csv"
    )

    importer = FlemishMemberImporter(
        str(filename), owner, CountryDbRepository(database)
    )

    command = ImportMembersCommand(preview=True)
    presenter = DummyPresenter()
    await ImportMembers(
        importer,
        FileUploadPreviewRepository(),
        MemberDbRepository(database),
        presenter,
    ).execute(command)

    assert presenter.count > 0, "There should be a member uploaded."


async def test_import_duplicate_members(database: Database, owner: Owner):
    """Test the use case Import Members."""
    filename = (
        Path(__file__).parent
        / "repositories"
        / "data"
        / "flemish_members_duplicate_test.csv"
    )

    importer = FlemishMemberImporter(
        str(filename), owner, CountryDbRepository(database)
    )

    command = ImportMembersCommand()
    presenter = DummyPresenter()
    with pytest.raises(DuplicateMemberUploadedException):
        await ImportMembers(
            importer,
            FileUploadDbRepository(database),
            MemberDbRepository(database),
            presenter,
        ).execute(command)
