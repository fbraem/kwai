"""Module for defining the endpoints for members of the club API."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.club.presenters import JsonApiMemberPresenter, JsonApiMembersPresenter
from kwai.api.v1.club.schemas.member import MemberDocument
from kwai.core.json_api import PaginationModel
from kwai.modules.club.get_member import GetMember, GetMemberCommand
from kwai.modules.club.get_members import GetMembers, GetMembersCommand
from kwai.modules.club.repositories.member_db_repository import MemberDbRepository
from kwai.modules.club.repositories.member_repository import MemberNotFoundException
from kwai.modules.identity.users.user import UserEntity


router = APIRouter()


class MembersFilterModel(BaseModel):
    """Define the JSON:API filter for members."""

    enabled: bool = Field(Query(default=True, alias="filter[enabled]"))
    license_end_month: int = Field(Query(default=0, alias="filter[license_end_month]"))
    license_end_year: int = Field(Query(default=0, alias="filter[license_end_year]"))


@router.get("/members")
async def get_members(
    pagination: PaginationModel = Depends(PaginationModel),
    members_filter: MembersFilterModel = Depends(MembersFilterModel),
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> MemberDocument:
    """Get members."""
    command = GetMembersCommand(
        offset=pagination.offset or 0,
        limit=pagination.limit or 0,
        active=members_filter.enabled,
        license_end_year=members_filter.license_end_year,
        license_end_month=members_filter.license_end_month,
    )
    presenter = JsonApiMembersPresenter()
    await GetMembers(MemberDbRepository(db), presenter).execute(command)

    return presenter.get_document()


@router.get("/members/{uuid}")
async def get_member(
    uuid: str,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> MemberDocument:
    """Get a member with the given unique id."""
    command = GetMemberCommand(uuid=uuid)

    presenter = JsonApiMemberPresenter()
    try:
        await GetMember(MemberDbRepository(db), presenter).execute(command)
    except MemberNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    return presenter.get_document()
