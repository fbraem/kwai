"""Module that defines the teams API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.teams.presenters import (
    JsonApiTeamMembersPresenter,
    JsonApiTeamPresenter,
    JsonApiTeamsPresenter,
)
from kwai.api.v1.teams.schemas import TeamDocument, TeamMemberDocument
from kwai.core.db.database import Database
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.teams.delete_team import DeleteTeam, DeleteTeamCommand
from kwai.modules.teams.get_team import GetTeam, GetTeamCommand
from kwai.modules.teams.get_teams import GetTeams, GetTeamsCommand
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository
from kwai.modules.training.teams.team_repository import TeamNotFoundException

router = APIRouter(tags=["teams"])


@router.get("/teams")
async def get_teams(
    database: Annotated[Database, Depends(create_database)],
) -> TeamDocument:
    """Get all teams of the club."""
    presenter = JsonApiTeamsPresenter()
    command = GetTeamsCommand(offset=0, limit=0)
    await GetTeams(TeamDbRepository(database), presenter).execute(command)
    return presenter.get_document()


@router.get("/teams/{id}")
async def get_team(
    id: int,
    database: Annotated[Database, Depends(create_database)],
) -> TeamDocument:
    """Get the team with the given id."""
    presenter = JsonApiTeamPresenter()
    command = GetTeamCommand(id=id)
    await GetTeam(TeamDbRepository(database), presenter).execute(command)
    return presenter.get_document()


@router.get("/teams/{id}/members")
async def get_team_members(
    id: int,
    database: Annotated[Database, Depends(create_database)],
) -> TeamMemberDocument:
    """Get the member of the team with the given id."""
    presenter = JsonApiTeamMembersPresenter()
    command = GetTeamCommand(id=id)
    await GetTeam(TeamDbRepository(database), presenter).execute(command)
    return presenter.get_document()


@router.delete(
    "/teams/{id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Team not found"}},
)
async def delete_team(
    id: int,
    database: Annotated[Database, Depends(create_database)],
    user: Annotated[UserEntity, Depends(get_current_user)],
):
    """Delete the team with the given id."""
    command = DeleteTeamCommand(id=id)

    try:
        await DeleteTeam(TeamDbRepository(database)).execute(command)
    except TeamNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
