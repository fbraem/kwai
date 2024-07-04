"""Module that defines the teams API."""

from typing import Annotated

from fastapi import APIRouter, Depends

from kwai.api.dependencies import create_database
from kwai.api.v1.teams.presenters import JsonApiTeamPresenter, JsonApiTeamsPresenter
from kwai.api.v1.teams.schemas import TeamDocument
from kwai.core.db.database import Database
from kwai.modules.teams.get_team import GetTeam, GetTeamCommand
from kwai.modules.teams.get_teams import GetTeams, GetTeamsCommand
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository

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
