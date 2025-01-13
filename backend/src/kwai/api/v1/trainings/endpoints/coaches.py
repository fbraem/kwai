"""Module for defining endpoints for coaches."""

from typing import Annotated

from fastapi import APIRouter, Depends

from kwai.api.dependencies import create_database
from kwai.api.v1.trainings.schemas.coach import CoachDocument
from kwai.core.db.database import Database
from kwai.core.json_api import Meta
from kwai.modules.training.coaches.coach_db_repository import CoachDbRepository
from kwai.modules.training.get_coaches import GetCoaches, GetCoachesCommand


router = APIRouter()


@router.get("/trainings/coaches")
async def get_coaches(
    database: Annotated[Database, Depends(create_database)],
) -> CoachDocument:
    """Get coaches."""
    count, coach_iterator = await GetCoaches(CoachDbRepository(database)).execute(
        GetCoachesCommand(active=True)
    )

    document = CoachDocument(meta=Meta(count=count), data=[])
    async for coach in coach_iterator:
        document.merge(CoachDocument.create(coach))

    return document
