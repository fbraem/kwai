"""Tests for the use case: get applications."""
from types import AsyncGeneratorType

import pytest

from kwai.core.db.database import Database
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
)
from kwai.modules.portal.get_applications import GetApplications, GetApplicationsCommand

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def repo(database: Database) -> ApplicationRepository:
    """Create an application repository."""
    return ApplicationDbRepository(database)


async def test_get_applications(repo: ApplicationRepository):
    """Test the use case: get applications."""
    command = GetApplicationsCommand()
    count, applications = await GetApplications(repo).execute(command)

    assert count >= 0, "Count must be 0 or greater"
    assert isinstance(
        applications, AsyncGeneratorType
    ), "A list of entities should be yielded"
