import pytest

from kwai.core.db.database import Database
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.applications.application_repository import (
    ApplicationRepository,
    ApplicationNotFoundException,
)


@pytest.fixture(scope="module")
def repo(database: Database) -> ApplicationRepository:
    """Fixture for an application repository."""
    return ApplicationDbRepository(database)


@pytest.fixture(scope="module")
async def application(repo: ApplicationRepository) -> ApplicationEntity:
    """Fixture for an application"""
    application = ApplicationEntity(
        title="Test", name="test", short_description="An application used for testing"
    )
    return await repo.create(application)


def test_create(application: ApplicationEntity):
    """Test if the application was created."""
    assert not application.id.is_empty(), "There should be an application created"


@pytest.mark.asyncio
async def test_get_by_id(repo: ApplicationRepository, application: ApplicationEntity):
    """Test if the application can be found with the id."""
    entity = await repo.get_by_id(application.id)
    assert entity.id == application.id, "The application should be found"


@pytest.mark.asyncio
async def test_get_by_name(repo: ApplicationRepository, application: ApplicationEntity):
    """Test if the application can be found with the name."""
    entity = await repo.get_by_name(application.name)
    assert entity.id == application.id, "The application should be found using the name"


@pytest.mark.asyncio
async def test_delete(repo: ApplicationRepository, application: ApplicationEntity):
    """Test if the application can be deleted."""
    await repo.delete(application)

    with pytest.raises(ApplicationNotFoundException):
        await repo.get_by_id(application.id)
