"""Module that implements invitations endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger

from kwai.api.dependencies import create_database, get_current_user, get_publisher
from kwai.api.v1.auth.schemas.user_invitation import UserInvitationDocument
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import InvalidEmailException
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.identity.delete_user_invitation import (
    DeleteUserInvitation,
    DeleteUserInvitationCommand,
)
from kwai.modules.identity.get_invitations import GetInvitations, GetInvitationsCommand
from kwai.modules.identity.get_user_invitation import (
    GetUserInvitation,
    GetUserInvitationCommand,
)
from kwai.modules.identity.invite_user import InviteUser, InviteUserCommand
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationNotFoundException,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_db_repository import UserDbRepository

router = APIRouter()


@router.post("/invitations")
async def create_user_invitation(
    user_invitation_document: UserInvitationDocument,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
    publisher=Depends(get_publisher),
) -> UserInvitationDocument:
    """Create a user invitation."""
    command = InviteUserCommand(
        first_name=user_invitation_document.resource.attributes.first_name,
        last_name=user_invitation_document.resource.attributes.last_name,
        email=user_invitation_document.resource.attributes.email,
        remark=user_invitation_document.resource.attributes.remark,
    )

    try:
        invitation = await InviteUser(
            user, UserDbRepository(db), UserInvitationDbRepository(db), publisher
        ).execute(command)
    except InvalidEmailException as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email address",
        ) from exc
    except UnprocessableException as ex:
        logger.warning(f"User invitation could not be processed: {ex}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex)
        ) from ex

    return UserInvitationDocument.create(invitation)


@router.delete(
    "/invitations/{uuid}",
    summary="Delete a user invitation",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
async def delete_user_invitation(
    uuid: str,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
):
    """Delete the user invitation with the given unique id."""
    command = DeleteUserInvitationCommand(uuid=uuid)
    try:
        await DeleteUserInvitation(UserInvitationDbRepository(db)).execute(command)
    except UserInvitationNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex)
        ) from ex


@router.get("/invitations")
async def get_user_invitations(
    pagination: PaginationModel = Depends(PaginationModel),
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> UserInvitationDocument:
    """Get all user invitations."""
    command = GetInvitationsCommand(offset=pagination.offset, limit=pagination.limit)
    count, invitation_iterator = await GetInvitations(
        UserInvitationDbRepository(db)
    ).execute(command)

    result = UserInvitationDocument(
        meta=Meta(count=count, limit=pagination.limit, offset=pagination.offset),
        data=[],
    )

    async for invitation in invitation_iterator:
        result.merge(UserInvitationDocument.create(invitation))

    return result


@router.get("/invitations/{uuid}")
async def get_user_invitation(
    uuid: str,
    db=Depends(create_database),
    user: UserEntity = Depends(get_current_user),
) -> UserInvitationDocument:
    """Get the user invitation with the given unique id."""
    command = GetUserInvitationCommand(uuid=uuid)
    try:
        invitation = await GetUserInvitation(UserInvitationDbRepository(db)).execute(
            command
        )
    except UserInvitationNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex

    return UserInvitationDocument.create(invitation)
