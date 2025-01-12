"""Module that defines tests for application database repository."""

import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.identifier import IntIdentifier
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)
from kwai.modules.portal.applications.application_repository import (
    ApplicationNotFoundException,
    ApplicationRepository,
)


pytestmark = pytest.mark.db


def find(entity_list: list, id_: IntIdentifier):
    """Search for an entity with the given id."""
    for entity in entity_list:
        if entity.id == id_:
            return entity
    return None


@pytest.fixture(scope="module")
def repo(database: Database) -> ApplicationRepository:
    """Fixture for an application repository."""
    return ApplicationDbRepository(database)


@pytest.fixture(scope="module")
async def application(repo: ApplicationRepository) -> ApplicationEntity:
    """Fixture for an application."""
    application = ApplicationEntity(
        title="Test",
        name="test_repo",
        short_description="An application used for testing",
    )
    return await repo.create(application)


def test_create(application: ApplicationEntity):
    """Test if the application was created."""
    assert not application.id.is_empty(), "There should be an application created"


async def test_get_by_id(repo: ApplicationRepository, application: ApplicationEntity):
    """Test if the application can be found with the id."""
    entity = await repo.get_by_id(application.id)
    assert entity.id == application.id, "The application should be found"


async def test_get_by_name(repo: ApplicationRepository, application: ApplicationEntity):
    """Test if the application can be found with the name."""
    entity = await repo.get_by_name(application.name)
    assert entity.id == application.id, "The application should be found using the name"


async def test_query_for_news(
    repo: ApplicationRepository, application: ApplicationEntity
):
    """Test if application can be found that can contain news."""
    query = repo.create_query()
    query.filter_only_news()
    entities = [entity async for entity in repo.get_all(query)]
    assert len(entities) > 0, "There should be an application"

    entity = find(entities, application.id)
    assert entity is not None, "The application should be found when looking for news"


async def test_query_for_pages(
    repo: ApplicationRepository, application: ApplicationEntity
):
    """Test if application can be found that can contain pages."""
    query = repo.create_query()
    query.filter_only_pages()
    entities = [entity async for entity in repo.get_all(query)]
    assert len(entities) > 0, "There should be an application"

    entity = find(entities, application.id)
    assert entity is not None, "The application should be found when looking for pages"


async def test_query_for_events(
    repo: ApplicationRepository, application: ApplicationEntity
):
    """Test if application can be found that can contain events."""
    query = repo.create_query()
    query.filter_only_events()
    entities = [entity async for entity in repo.get_all(query)]
    assert len(entities) > 0, "There should be an application"

    entity = find(entities, application.id)
    assert entity is not None, "The application should be found when looking for events"


async def test_delete(repo: ApplicationRepository, application: ApplicationEntity):
    """Test if the application can be deleted."""
    await repo.delete(application)

    with pytest.raises(ApplicationNotFoundException):
        await repo.get_by_id(application.id)
