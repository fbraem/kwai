"""Module that implement all users endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.auth.presenters import (
    JsonApiUserAccountPresenter,
    JsonApiUserAccountsPresenter,
)
from kwai.api.v1.auth.schemas.user_account import (
    CreateUserAccountResource,
    UserAccountDocument,
)
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.core.domain.exceptions import UnprocessableException
from kwai.core.json_api import PaginationModel, SingleDocument
from kwai.modules.identity.accept_user_invitation import (
    AcceptUserInvitation,
    AcceptUserInvitationCommand,
)
from kwai.modules.identity.get_user_accounts import (
    GetUserAccounts,
    GetUserAccountsCommand,
)
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationNotFoundException,
)
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


router = APIRouter()


@router.get(
    "",
    summary="Get all users",
    responses={
        200: {"description": "Ok."},
        401: {"description": "Not Authorized."},
    },
)
async def get(
    database: Annotated[Database, Depends(create_database)],
    pagination: Annotated[PaginationModel, Depends(PaginationModel)],
    user: Annotated[UserEntity, Depends(get_current_user)],
):
    """Get all user accounts."""
    command = GetUserAccountsCommand(
        offset=pagination.offset or 0, limit=pagination.limit or 0
    )
    presenter = JsonApiUserAccountsPresenter()
    await GetUserAccounts(UserAccountDbRepository(database), presenter).execute(command)
    return presenter.get_document()


@router.post(
    "",
    summary="Create a new user account",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User account created"},
        400: {"description": "Wrong or missing user invitation relationship"},
        404: {"description": "User invitation does not exist"},
        422: {"description": "Invalid email address or user invitation was invalid"},
    },
)
async def create_user_account(
    document: SingleDocument[CreateUserAccountResource, None],
    database: Annotated[Database, Depends(create_database)],
) -> UserAccountDocument:
    """Create a new user account.

    A user account can only be created when a related user invitation
    is not yet expired.
    """
    if (
        document.data.relationships is None
        or document.data.relationships.user_invitation.data is None
        or isinstance(document.data.relationships.user_invitation.data, list)
        or document.data.relationships.user_invitation.data.id is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong or missing user_invitation relationship",
        )

    command = AcceptUserInvitationCommand(
        uuid=document.data.relationships.user_invitation.data.id,
        first_name=document.data.attributes.first_name,
        last_name=document.data.attributes.last_name,
        password=document.data.attributes.password,
        remark=document.data.attributes.remark,
    )

    presenter = JsonApiUserAccountPresenter()
    async with UnitOfWork(database):
        try:
            await AcceptUserInvitation(
                UserInvitationDbRepository(database),
                UserAccountDbRepository(database),
                presenter,
            ).execute(command)
        except UnprocessableException as exc:
            logger.warning(f"User account could not be created: {exc}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
            ) from exc
        except UserInvitationNotFoundException as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
            ) from exc

    result = presenter.get_document()
    assert result, "There is no document created yet"
    return result
