"""Module that defines fixtures for the stories module."""
import pytest

from kwai.core.db.database import Database
from kwai.modules.identity.users.user import UserEntity
from kwai.modules.news.stories.story import Application, Author
from kwai.modules.portal.applications.application import ApplicationEntity
from kwai.modules.portal.applications.application_db_repository import (
    ApplicationDbRepository,
)


@pytest.fixture(scope="module")
async def author(user: UserEntity) -> Author:
    """Fixture for an author."""
    return Author(id=user.id, uuid=user.uuid, name=user.name)


@pytest.fixture(scope="module")
async def application(database: Database) -> Application:
    """Fixture for an application."""
    repo = ApplicationDbRepository(database)
    application = ApplicationEntity(
        title="Test", name="test", short_description="An application used for testing"
    )
    application = await repo.create(application)

    yield Application(id=application.id, name=application.name, title=application.title)

    await repo.delete(application)
