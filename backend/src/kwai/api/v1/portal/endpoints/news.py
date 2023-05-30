"""Module that implements news endpoints."""
from fastapi import APIRouter

from kwai.api.dependencies import deps
from kwai.api.schemas.jsonapi import Meta
from kwai.api.v1.portal.schemas.story import (
    PortalStoryData,
    PortalStoryAttributes,
    PortalStoriesDocument,
    PortalStoryContent,
)
from kwai.core.db.database import Database
from kwai.modules.news.get_stories import GetStoriesCommand, GetStories
from kwai.modules.news.stories.story import StoryEntity
from kwai.modules.news.stories.story_db_repository import StoryDbRepository

router = APIRouter()


def _create_story_data(story: StoryEntity) -> PortalStoryData:
    return PortalStoryData(
        id=str(story.id),
        attributes=PortalStoryAttributes(
            content=[
                PortalStoryContent(
                    locale=content.locale,
                    title=content.title,
                    summary=content.summary,
                    content=content.content,
                )
                for content in story.content
            ],
            publish_date=str(story.period.start_date),
            promotion=story.promotion.priority,
        ),
    )


@router.get("/news")
async def get_news(db=deps.depends(Database)) -> PortalStoriesDocument:
    """Get news stories for the portal."""
    command = GetStoriesCommand()
    count, story_iterator = await GetStories(StoryDbRepository(db)).execute(command)

    result: list[PortalStoryData] = []
    async for story in story_iterator:
        result.append(_create_story_data(story))

    return PortalStoriesDocument(meta=Meta(count=count), data=result)
