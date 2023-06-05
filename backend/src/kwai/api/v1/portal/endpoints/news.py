"""Module that implements news endpoints."""
from typing import AsyncIterator

from fastapi import APIRouter, Depends

from kwai.api.dependencies import deps
from kwai.api.schemas.application import ApplicationResourceIdentifier
from kwai.api.schemas.jsonapi import PaginationModel, Meta
from kwai.api.v1.portal.schemas.story import (
    PortalStoryData,
    PortalStoryAttributes,
    PortalStoriesDocument,
    PortalStoryContent,
    PortalStoryApplicationData,
    PortalStoryApplicationAttributes,
    RelationshipData,
    PortalStoryRelationships,
)
from kwai.core.db.database import Database
from kwai.modules.news.get_stories import GetStoriesCommand, GetStories
from kwai.modules.news.stories.story import StoryEntity
from kwai.modules.news.stories.story_db_repository import StoryDbRepository

router = APIRouter()


class PortalStoryResource:
    def __init__(self):
        pass

    async def serialize(self, iterator: AsyncIterator) -> PortalStoriesDocument:
        result: list[PortalStoryData] = []
        included: set[PortalStoryApplicationData] = set()
        async for story in iterator:
            result.append(_create_story_data(story))
            included.add(
                PortalStoryApplicationData(
                    id=story.application.id.value,
                    attributes=PortalStoryApplicationAttributes(
                        name=story.application.name,
                        title=story.application.title,
                    ),
                )
            )

        return PortalStoriesDocument(
            data=result,
            included=included,
        )


def _create_story_data(story: StoryEntity) -> PortalStoryData:
    return PortalStoryData(
        id=str(story.id),
        attributes=PortalStoryAttributes(
            priority=story.promotion.priority,
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
        ),
        relationships=PortalStoryRelationships(
            application=RelationshipData(
                data=ApplicationResourceIdentifier(id=story.application.id.value)
            )
        ),
    )


@router.get("/news")
async def get_news(
    pagination: PaginationModel = Depends(PaginationModel), db=deps.depends(Database)
) -> PortalStoriesDocument:
    """Get news stories for the portal.

    Only promoted news stories are returned for the portal.
    """
    command = GetStoriesCommand(
        offset=pagination.offset or 0, limit=pagination.limit or 10, promoted=True
    )
    count, story_iterator = await GetStories(StoryDbRepository(db)).execute(command)

    result: PortalStoriesDocument = await PortalStoryResource().serialize(
        story_iterator
    )
    result.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return result
