"""Module for testing the "Create Page" use case."""
from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.create_page import CreatePage, CreatePageCommand
from kwai.modules.portal.page_command import TextCommand
from kwai.modules.portal.pages.page_repository import PageRepository


async def test_create_page(
    repo: PageRepository,
    application: ApplicationEntity,
    application_repo: ApplicationRepository,
    owner: Owner,
):
    """Test "Create Page" use case."""
    command = CreatePageCommand(
        enabled=True,
        text=[
            TextCommand(
                locale="nl",
                format="md",
                title="Test",
                summary="This is a test page",
                content="This is a test page",
            ),
        ],
        application=application.id.value,
        priority=0,
        remark="This is a test page created with test_create_page.",
    )
    page = await CreatePage(repo, application_repo, owner).execute(command)
    assert page is not None, "There should be a page."
