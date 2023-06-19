"""Module that implements news endpoints."""
from abc import ABC, abstractmethod

import markdown
from fastapi import APIRouter, Depends

from kwai.api.dependencies import deps
from kwai.api.schemas.jsonapi import Meta, PaginationModel
from kwai.api.v1.portal.schemas.story import PortalStoryResource
from kwai.core.db.database import Database
from kwai.modules.news.get_stories import GetStories, GetStoriesCommand
from kwai.modules.news.stories.story_db_repository import StoryDbRepository

router = APIRouter()

# pylint: disable=too-few-public-methods


class DocumentConverter(ABC):
    """Interface for a document converter.

    A converter will convert a certain format (markdown for example) into HTML.
    """

    @abstractmethod
    def convert(self, content: str) -> str:
        """Convert a string to HTML."""
        raise NotImplementedError


class MarkdownConverter(DocumentConverter):
    """Converter for converting markdown into HTML."""

    def convert(self, content: str) -> str:
        """Convert markdown to HTML."""
        return markdown.markdown(content)


@router.get("/news")
async def get_news(
    pagination: PaginationModel = Depends(PaginationModel), db=deps.depends(Database)
) -> PortalStoryResource.__json_api_resource__.get_document_model():
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
    document.meta = Meta(
        count=count, offset=command.offset, limit=command.limit, test="Hoi!"
    )

    return document
