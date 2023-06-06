"""Module that implements news endpoints."""
from abc import ABC, abstractmethod
from typing import AsyncIterator

import markdown
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


class DocumentConverter(ABC):
    @abstractmethod
    def convert(self, content: str) -> str:
        raise NotImplementedError


class MarkdownConverter(DocumentConverter):
    def convert(self, content: str) -> str:
        return markdown.markdown(content)


class PortalStoryResource:
    def __init__(self, story: StoryEntity):
        self._story = story

    def _create_story_data(self) -> tuple[PortalStoryData, PortalStoryApplicationData]:
        return (
            PortalStoryData(
                id=str(self._story.id),
                attributes=PortalStoryAttributes(
                    priority=self._story.promotion.priority,
                    content=[
                        PortalStoryContent(
                            locale=content.locale,
                            title=content.title,
                            summary=MarkdownConverter().convert(content.summary),
                            content=MarkdownConverter().convert(content.content)
                            if content.content
                            else None,
                        )
                        for content in self._story.content
                    ],
                    publish_date=str(self._story.period.start_date),
                ),
                relationships=PortalStoryRelationships(
                    application=RelationshipData(
                        data=ApplicationResourceIdentifier(
                            id=self._story.application.id.value
                        )
                    )
                ),
            ),
            PortalStoryApplicationData(
                id=self._story.application.id.value,
                attributes=PortalStoryApplicationAttributes(
                    name=self._story.application.name,
                    title=self._story.application.title,
                ),
            ),
        )

    @classmethod
    async def serialize(cls, iterator: AsyncIterator) -> PortalStoriesDocument:
        result: list[PortalStoryData] = []
        included: set[PortalStoryApplicationData] = set()
        async for story in iterator:
            story_data, application_data = PortalStoryResource(
                story
            )._create_story_data()
            result.append(story_data)
            included.add(application_data)

        return PortalStoriesDocument(
            data=result,
            included=included,
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

    result: PortalStoriesDocument = await PortalStoryResource.serialize(story_iterator)
    result.meta = Meta(count=count, offset=command.offset, limit=command.limit)

    return result
