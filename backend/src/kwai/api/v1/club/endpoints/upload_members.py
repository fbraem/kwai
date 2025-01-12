"""Module that defines the members API."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.club.presenters import JsonApiUploadMemberPresenter
from kwai.api.v1.club.schemas.member import MemberDocument
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.functions import generate_filenames
from kwai.core.settings import Settings, get_settings
from kwai.modules.club.import_members import (
    ImportMembers,
    ImportMembersCommand,
)
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
from kwai.modules.identity.users.user import UserEntity

router = APIRouter()


class UploadMemberModel(BaseModel):
    """Model containing information about a row.

    The id will be set, when a member is successfully imported. When a member was
    not imported, the message will contain a description about the problem.
    """

    row: int
    id: int | None = None
    message: str = ""


class UploadMembersModel(BaseModel):
    """Model that contains the information about all rows."""

    members: list[UploadMemberModel] = Field(default_factory=list)


@router.post("/members/upload")
async def upload(
    member_file: Annotated[
        UploadFile, File(description="A file with members to upload into kwai")
    ],
    settings: Annotated[Settings, Depends(get_settings)],
    database: Annotated[Database, Depends(create_database)],
    user: Annotated[UserEntity, Depends(get_current_user)],
    preview: Annotated[bool, Query(description="Whether or not to preview")] = True,
) -> MemberDocument:
    """Upload a members csv file."""
    if member_file.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no filename available for the uploaded file.",
        )

    try:
        member_filename = await upload_file(member_file, settings.files.path)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload members file: {ex}",
        ) from ex

    presenter = JsonApiUploadMemberPresenter()
    async with UnitOfWork(database):
        try:
            await ImportMembers(
                FlemishMemberImporter(
                    str(member_filename),
                    user.create_owner(),
                    CountryDbRepository(database),
                ),
                (
                    FileUploadPreviewRepository()
                    if preview
                    else FileUploadDbRepository(database)
                ),
                MemberDbRepository(database),
                presenter,
            ).execute(ImportMembersCommand(preview=preview))
        except DuplicateMemberUploadedException as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to upload members file: {ex}",
            ) from ex

    return presenter.get_document()


async def upload_file(uploaded_file, path: str):
    """Creates a unique file for the uploaded file."""
    file_path = Path(path)
    file_path.mkdir(parents=True, exist_ok=True)
    member_file_path = file_path / uploaded_file.filename
    member_filename_generator = generate_filenames(
        member_file_path.stem + "_", member_file_path.suffix
    )
    while True:
        member_filename = file_path / next(member_filename_generator)
        if not member_filename.exists():
            break

    with open(member_filename, "wb") as fh:
        fh.write(await uploaded_file.read())

    return member_filename
