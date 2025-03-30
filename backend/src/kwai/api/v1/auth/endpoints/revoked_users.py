"""Module that implements endpoints for revoke users."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.auth.presenters import JsonApiRevokedUserPresenter
from kwai.api.v1.auth.schemas.revoked_user import RevokedUserDocument
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.modules.identity.enact_user import EnactUser, EnactUserCommand
from kwai.modules.identity.revoke_user import RevokeUser, RevokeUserCommand
from kwai.modules.identity.tokens.user_token_db_repository import UserTokenDbRepository
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.identity.users.user_account_db_repository import (
    UserAccountDbRepository,
)


router = APIRouter()


@router.post(
    "/revoked_users",
    summary="Revoke a user",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User was successfully revoked"},
        400: {"description": "An invalid request was made"},
        401: {"description": "Not authorized"},
    },
)
async def post(
    document: RevokedUserDocument,
    database: Annotated[Database, Depends(create_database)],
    user: Annotated[UserEntity, Depends(get_current_user)],
) -> RevokedUserDocument:
    """(Un)revoke a user."""
    if document.resource.id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The revoked user resource must have an id",
        )
    presenter = JsonApiRevokedUserPresenter()
    if document.resource.attributes.revoked:
        async with UnitOfWork(database):
            await RevokeUser(
                UserAccountDbRepository(database),
                UserTokenDbRepository(database),
                presenter,
            ).execute(RevokeUserCommand(uuid=document.resource.id))
    else:
        async with UnitOfWork(database):
            await EnactUser(UserAccountDbRepository(database), presenter).execute(
                EnactUserCommand(uuid=document.resource.id)
            )
    return presenter.get_document()


@router.delete(
    "/revoked_users/{id}",
    summary="Cancel the revocation of a user",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "The revocation was successfully cancelled"},
        401: {"description": "Not authorized"},
    },
)
async def delete(
    id: str,
    database: Annotated[Database, Depends(create_database)],
    user: Annotated[UserEntity, Depends(get_current_user)],
):
    """Cancel the revocation of the user with the given id."""
    presenter = JsonApiRevokedUserPresenter()
    async with UnitOfWork(database):
        await EnactUser(UserAccountDbRepository(database), presenter).execute(
            EnactUserCommand(uuid=id)
        )
