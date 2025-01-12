"""Tests for the use case: get application."""

import pytest

from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.get_application import GetApplication, GetApplicationCommand

pytestmark = pytest.mark.db


async def test_get_applications(
    application_repo: ApplicationRepository, application: ApplicationEntity
):
    """Test the use case: get application."""
    command = GetApplicationCommand(id=application.id.value)
    application = await GetApplication(application_repo).execute(command)

    assert application is not None, "There should be an application"
