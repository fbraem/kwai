"""Module that defines the teams API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from kwai.api.dependencies import create_database, get_current_user
from kwai.api.v1.teams.presenters import (
    JsonApiTeamMemberPresenter,
    JsonApiTeamMembersPresenter,
    JsonApiTeamPresenter,
    JsonApiTeamsPresenter,
)
from kwai.api.v1.teams.schemas import TeamDocument, TeamMemberDocument
from kwai.core.db.database import Database
from kwai.core.db.uow import UnitOfWork
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.teams.create_team import CreateTeam, CreateTeamCommand
from kwai.modules.teams.create_team_member import (
    CreateTeamMember,
    CreateTeamMemberCommand,
)
from kwai.modules.teams.delete_team import DeleteTeam, DeleteTeamCommand
from kwai.modules.teams.domain.team import TeamMemberAlreadyExistException
from kwai.modules.teams.get_team import GetTeam, GetTeamCommand
from kwai.modules.teams.get_teams import GetTeams, GetTeamsCommand
from kwai.modules.teams.repositories.member_db_repository import MemberDbRepository
from kwai.modules.teams.repositories.member_repository import MemberNotFoundException
from kwai.modules.teams.repositories.team_db_repository import TeamDbRepository
from kwai.modules.teams.update_team import UpdateTeam, UpdateTeamCommand
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


@router.post("/teams", status_code=status.HTTP_201_CREATED)
async def create_team(
    resource: TeamDocument,
    database: Annotated[Database, Depends(create_database)],
    user: Annotated[UserEntity, Depends(get_current_user)],
) -> TeamDocument:
    """Create a new team."""
    command = CreateTeamCommand(
        name=resource.data.attributes.name,
        active=resource.data.attributes.active,
        remark=resource.data.attributes.remark,
    )
    team_presenter = JsonApiTeamPresenter()
    async with UnitOfWork(database):
        await CreateTeam(TeamDbRepository(database), team_presenter).execute(command)
    return team_presenter.get_document()


@router.patch(
    "/teams/{id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Team not found"}},
)
async def update_team(
    id: int,
    resource: TeamDocument,
    database: Annotated[Database, Depends(create_database)],
    user: Annotated[UserEntity, Depends(get_current_user)],
) -> TeamDocument:
    """Update an existing team."""
    command = UpdateTeamCommand(
        id=id,
        name=resource.data.attributes.name,
        active=resource.data.attributes.active,
        remark=resource.data.attributes.remark,
    )
    team_presenter = JsonApiTeamPresenter()
    async with UnitOfWork(database):
        await UpdateTeam(TeamDbRepository(database), team_presenter).execute(command)
    return team_presenter.get_document()


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
        async with UnitOfWork(database):
            await DeleteTeam(TeamDbRepository(database)).execute(command)
    except TeamNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex


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


@router.post("/teams/{id}/members", status_code=status.HTTP_201_CREATED)
async def create_team_member(
    id: int,
    resource: TeamMemberDocument,
    database: Annotated[Database, Depends(create_database)],
) -> TeamMemberDocument:
    """Add a member to the team with the given id."""
    presenter = JsonApiTeamMemberPresenter()
    command = CreateTeamMemberCommand(
        team_id=id,
        member_id=resource.data.id,
        active=resource.data.attributes.active,
    )
    try:
        async with UnitOfWork(database):
            await CreateTeamMember(
                TeamDbRepository(database), MemberDbRepository(database), presenter
            ).execute(command)
            return presenter.get_document()
    except TeamNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
    except MemberNotFoundException as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(ex)
        ) from ex
    except TeamMemberAlreadyExistException as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ex)
        ) from ex
