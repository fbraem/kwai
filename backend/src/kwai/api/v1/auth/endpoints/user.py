"""Module that implements all user endpoints."""

from fastapi import APIRouter, Depends

from kwai.api.dependencies import get_current_user, deps
from kwai.api.schemas.user_invitation import UserInvitationSchema
from kwai.core.db.database import Database
from kwai.core.json_api import JsonApiDocument, Document
from kwai.modules.identity.invite_user import InviteUserCommand, InviteUser
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_db_repository import UserDbRepository

router = APIRouter()


@router.get("/user")
def get(user: UserEntity = Depends(get_current_user)):
    """Get the current user."""
    return {"id": str(user.uuid)}


@router.post("/users/invitations")
def create_user_invitation(
    db=deps.depends(Database), user: UserEntity = Depends(get_current_user)
) -> JsonApiDocument:
    """Create a user invitation."""
    command = InviteUserCommand(
        first_name="",
        last_name="",
        email="",
    )
    invitation = InviteUser(
        user, UserDbRepository(db), InvitationDbRepository(db)
    ).execute(command)

    return Document(
        UserInvitationSchema(
            id=str(invitation.id.value),
            email=str(invitation.email),
            first_name=invitation.name.first_name,
            last_name=invitation.name.last_name,
            remark=invitation.remark,
            expired_at=str(invitation.expired_at),
            confirmed_at=None
            if invitation.confirmed_at.empty
            else str(invitation.confirmed_at),
            created_at=str(invitation.traceable_time.created_at),
            updated_at=None
            if invitation.traceable_time.updated_at
            else str(invitation.traceable_time.updated_at),
        )
    ).serialize()
