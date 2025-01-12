"""Module for testing the "Update Page" use case."""

from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.page_command import TextCommand
from kwai.modules.portal.pages.page import PageEntity
from kwai.modules.portal.pages.page_repository import PageRepository
from kwai.modules.portal.update_page import UpdatePage, UpdatePageCommand


async def test_update_page(
    page_repo: PageRepository,
    application_repo: ApplicationRepository,
    owner: Owner,
    saved_page: PageEntity,
):
    """Test the "Update Page" use case."""
    command = UpdatePageCommand(
        id=saved_page.id.value,
        enabled=saved_page.enabled,
        texts=[
            TextCommand(
                locale=text.locale.value,
                format=text.format.value,
                title=text.title,
                summary=text.summary,
                content=text.content,
            )
            for text in saved_page.texts
        ],
        application=saved_page.application.id.value,
        priority=saved_page.priority,
        remark="Updated with test_update_page",
    )
    updated_page = await UpdatePage(page_repo, application_repo, owner).execute(command)
    assert updated_page is not None, "There should be an updated page."
    assert updated_page.remark == "Updated with test_update_page", (
        "The page should be updated."
    )
