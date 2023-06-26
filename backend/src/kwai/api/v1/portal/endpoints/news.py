"""Module that implements news endpoints."""

from fastapi import APIRouter, Depends

from kwai.api.dependencies import deps
from kwai.api.v1.portal.schemas.story import PortalStoryResource
from kwai.core.db.database import Database
from kwai.core.json_api import Meta, PaginationModel
from kwai.modules.news.get_stories import GetStories, GetStoriesCommand
from kwai.modules.news.stories.story_db_repository import StoryDbRepository

router = APIRouter()


@router.get("/news")
async def get_news(
    pagination: PaginationModel = Depends(PaginationModel), db=deps.depends(Database)
) -> PortalStoryResource.get_document_model():
    """Get news stories for the portal.

    Only promoted news stories are returned for the portal.
    """
    command = GetStoriesCommand(
        offset=pagination.offset or 0, limit=pagination.limit or 10, promoted=True
    )
    count, story_iterator = await GetStories(StoryDbRepository(db)).execute(command)

    document = PortalStoryResource.serialize_list(
        [PortalStoryResource(story) async for story in story_iterator]
    )
    document.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return document
