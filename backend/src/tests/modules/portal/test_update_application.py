"""Module for testing the "Update Application" use case."""

from kwai.core.domain.value_objects.owner import Owner
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.update_application import (
    UpdateApplication,
    UpdateApplicationCommand,
)


async def test_update_application(
    application_repo: ApplicationRepository,
    owner: Owner,
    application: ApplicationEntity,
):
    """Test the "Update Application" use case."""
    command = UpdateApplicationCommand(
        id=application.id.value,
        title=application.title,
        short_description=application.short_description,
        description=application.description,
        weight=application.weight,
        events=application.can_contain_events,
        pages=application.can_contain_pages,
        news=application.can_contain_news,
        remark="Updated with test_update_application",
    )
    updated_page = await UpdateApplication(application_repo).execute(command)
    assert updated_page is not None, "There should be an updated application."
    assert updated_page.remark == "Updated with test_update_application", (
        "The application should be updated."
    )
