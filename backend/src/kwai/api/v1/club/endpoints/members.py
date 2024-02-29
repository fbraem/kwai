"""Module that defines the members API."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

from kwai.api.dependencies import create_database, get_current_user
from kwai.core.db.database import Database
from kwai.core.settings import Settings, get_settings
from kwai.modules.club.import_members import (
    FailureResult,
    ImportMembers,
    OkResult,
)
from kwai.modules.club.members.country_db_repository import CountryDbRepository
from kwai.modules.club.members.file_upload_db_repository import FileUploadDbRepository
from kwai.modules.club.members.flemish_member_importer import FlemishMemberImporter
from kwai.modules.club.members.member_db_repository import MemberDbRepository
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

    members: list[UploadMemberModel] = Field(..., default_factory=list)


@router.post("/members/upload")
async def upload(
    member_file: Annotated[
        UploadFile, File(description="A file with members to upload into kwai")
    ],
    settings: Annotated[Settings, Depends(get_settings)],
    database: Annotated[Database, Depends(create_database)],
    user: Annotated[UserEntity, Depends(get_current_user)],
) -> UploadMembersModel:
    """Upload a members csv file."""
    if member_file.filename is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is no filename available for the uploaded file.",
        )

    file_path = Path(settings.files.path)
    file_path.mkdir(parents=True, exist_ok=True)
    member_filename = file_path / member_file.filename
    with open(member_filename, "wb") as fh:
        fh.write(await member_file.read())

    response = UploadMembersModel()

    imported_member_generator = ImportMembers(
        FlemishMemberImporter(
            str(member_filename),
            user.create_owner(),
            CountryDbRepository(database),
        ),
        FileUploadDbRepository(database),
        MemberDbRepository(database),
    ).execute()

    async for result in imported_member_generator:
        match result:
            case OkResult():
                response.members.append(
                    UploadMemberModel(row=result.row, id=result.member.id.value)
                )
            case FailureResult():
                response.members.append(
                    UploadMemberModel(row=result.row, message=result.to_message())
                )
            case _:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Unexpected result returned",
                )
    return response
