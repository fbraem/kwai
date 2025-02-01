"""Module that implement all users endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.auth.presenters import JsonApiUserAccountsPresenter
from kwai.core.db.database import Database
from kwai.core.json_api import PaginationModel
from kwai.modules.identity.get_user_accounts import (
    GetUserAccounts,
    GetUserAccountsCommand,
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
