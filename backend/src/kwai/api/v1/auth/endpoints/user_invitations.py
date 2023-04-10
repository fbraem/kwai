"""Module that implements invitations endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from kwai.api.dependencies import get_current_user, deps
from kwai.api.schemas.jsonapi import PaginationModel, Meta
from kwai.api.schemas.user_invitation import (
    UserInvitationDocument,
    UserInvitationsDocument,
    UserInvitationData,
    UserInvitationAttributes,
)
from kwai.core.db.database import Database
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.domain.value_objects.email_address import InvalidEmailException
from kwai.core.events.bus import Bus
from kwai.modules.identity.get_invitations import GetInvitations, GetInvitationsCommand
from kwai.modules.identity.invite_user import InviteUserCommand, InviteUser
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_db_repository import UserDbRepository

router = APIRouter()


@router.post("/invitations")
async def create_user_invitation(
    resource: UserInvitationDocument,
    db=deps.depends(Database),
    user: UserEntity = Depends(get_current_user),
    bus=deps.depends(Bus),
) -> UserInvitationDocument:
    """Create a user invitation."""

    command = InviteUserCommand(
        first_name=resource.data.attributes.first_name,
        last_name=resource.data.attributes.last_name,
        email=resource.data.attributes.email,
    )

    try:
        invitation = await InviteUser(
            user, UserDbRepository(db), InvitationDbRepository(db), bus
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

    resource.data.id = str(invitation.id.value)
    resource.data.attributes.expired_at = str(invitation.expired_at)
    resource.data.attributes.created_at = str(invitation.traceable_time.created_at)

    return resource


@router.get("/invitations")
def get_user_invitations(
    pagination: PaginationModel = Depends(PaginationModel),
    db=deps.depends(Database),
    user: UserEntity = Depends(get_current_user),  # pylint: disable=unused-argument
) -> UserInvitationsDocument:
    """Get all user invitations."""
    command = GetInvitationsCommand(offset=pagination.offset, limit=pagination.limit)
    count, invitations = GetInvitations(InvitationDbRepository(db)).execute(command)

    result: list[UserInvitationData] = []

    for invitation in invitations:
        result.append(
            UserInvitationData(
                id=str(invitation.id.value),
                attributes=UserInvitationAttributes(
                    email=str(invitation.email),
                    first_name=invitation.name.first_name,
                    last_name=invitation.name.last_name,
                    remark=invitation.remark,
                    expired_at=str(invitation.expired_at),
                    confirmed_at=(
                        None
                        if invitation.confirmed_at.empty
                        else str(invitation.confirmed_at)
                    ),
                    created_at=str(invitation.traceable_time.created_at),
                    updated_at=(
                        None
                        if invitation.traceable_time.updated_at.empty
                        else str(invitation.traceable_time.updated_at)
                    ),
                ),
            )
        )

    return UserInvitationsDocument(
        meta=Meta(count=count, offset=pagination.offset or 0, limit=pagination.limit),
        data=result,
    )
