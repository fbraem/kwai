"""Module that defines the teams API."""

from fastapi import APIRouter

from kwai.api.v1.teams.schemas import TeamDocument

router = APIRouter(tags=["teams"])


@router.get("/teams")
async def get_teams() -> TeamDocument:
    """Get all teams of the club."""
