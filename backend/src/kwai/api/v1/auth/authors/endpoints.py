"""Module for defining endpoints for managing authors."""

from typing import Annotated

from fastapi import APIRouter, Depends

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.auth.authors.presenters import JsonApiAuthorsPresenter
from kwai.core.db.database import Database
from kwai.core.json_api import PaginationModel
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.portal.get_authors import GetAuthors, GetAuthorsCommand
from kwai.modules.portal.repositories.author_db_repository import AuthorDbRepository


router = APIRouter()


@router.get(
    "/authors",
    summary="Get all authors",
    responses={200: {"description": "Ok."}, 401: {"description": "Not Authorized."}},
)
async def get(
    database: Annotated[Database, Depends(create_database)],
    pagination: Annotated[PaginationModel, Depends(PaginationModel)],
    user: Annotated[UserEntity, Depends(get_current_user)],
):
    """Get all authors."""
    command = GetAuthorsCommand(
        offset=pagination.offset or 0, limit=pagination.limit or 0
    )
    presenter = JsonApiAuthorsPresenter()
    await GetAuthors(AuthorDbRepository(database), presenter).execute(command)
    return presenter.get_document()
