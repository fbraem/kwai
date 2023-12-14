"""Module for defining the trainings/teams API."""
from fastapi import APIRouter, Depends

from kwai.api.v1.trainings.schemas.team import TeamResource
from kwai.core.dependencies import create_database
from kwai.core.json_api import Meta
from kwai.modules.training.get_teams import GetTeams
from kwai.modules.training.teams.team_db_repository import TeamDbRepository

router = APIRouter()


@router.get("/trainings/teams")
async def get_teams(
    database=Depends(create_database),
) -> TeamResource.get_document_model():
    """Get teams."""
    count, team_iterator = await GetTeams(TeamDbRepository(database)).execute()
    document = TeamResource.serialize_list(
        [TeamResource(team) async for team in team_iterator]
    )
    document.meta = Meta(count=count)

    return document
