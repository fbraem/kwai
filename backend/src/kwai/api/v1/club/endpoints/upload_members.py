"""Module that defines the members API."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.club.schemas.member import MemberDocument
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.functions import generate_filenames
from kwai.core.json_api import Meta
from kwai.core.settings import Settings, get_settings
from kwai.modules.club.import_members import (
    FailureResult,
    ImportMembers,
    ImportMembersCommand,
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

    members: list[UploadMemberModel] = Field(default_factory=list)


@router.post("/members/upload")
async def upload(
    member_file: Annotated[
        UploadFile, File(description="A file with members to upload into kwai")
    ],
    settings: Annotated[Settings, Depends(get_settings)],
    database: Annotated[Database, Depends(create_database)],
    user: Annotated[UserEntity, Depends(get_current_user)],
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

    async with UnitOfWork(database):
        imported_member_generator = ImportMembers(
            FlemishMemberImporter(
                str(member_filename),
                user.create_owner(),
                CountryDbRepository(database),
            ),
            FileUploadDbRepository(database),
            MemberDbRepository(database),
        ).execute(ImportMembersCommand())

    meta = Meta(count=0, offset=0, limit=0, errors=[])
    response = MemberDocument(meta=meta, data=[])
    upload_entity = None
    async for result in imported_member_generator:
        if upload_entity is None:
            upload_entity = result.file_upload

        match result:
            case OkResult():
                member_document = MemberDocument.create(result.member)
                member_document.resource.meta.row = result.row
                member_document.resource.meta.new = not result.member.has_id()
                # A new member has related resources that are not saved yet,
                # so give them temporarily the same id as the member.
                if member_document.resource.meta.new:
                    member_document.resource.relationships.person.data.id = (
                        member_document.resource.id
                    )
                    for included in member_document.included:
                        if included.type == "persons":
                            included.relationships.contact.data.id = (
                                member_document.resource.id
                            )
                        if included.id == "0":
                            included.id = member_document.resource.id
                meta.count += 1
                response.merge(member_document)
            case FailureResult():
                meta.errors.append({"row": result.row, "message": result.to_message()})
            case _:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Unexpected result returned",
                )
    return response


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
