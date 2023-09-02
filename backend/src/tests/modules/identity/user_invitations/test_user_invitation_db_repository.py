"""Module for testing UserInvitationDbRepository."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.local_timestamp import LocalTimestamp
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    UserInvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationNotFoundException,
    UserInvitationRepository,
)
from kwai.modules.identity.users.user import UserEntity

pytestmark = pytest.mark.db


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Fixture for creating the invitation repository."""
    return UserInvitationDbRepository(database)


@pytest.fixture(scope="module")
async def invitation(
    repo: UserInvitationRepository, user: UserEntity
) -> UserInvitationEntity:
    """Fixture for an invitation."""
    invitation = UserInvitationEntity(
        email=EmailAddress("ichiro.abe@kwai.com"),
        name=Name(first_name="Ichiro", last_name="Abe"),
        remark="Created with pytest",
        user=user,
    )
    return await repo.create(invitation)


def test_create(invitation: UserInvitationEntity):
    """Test if the invitation was created."""
    assert not invitation.id.is_empty(), "There should be an invitation created"


async def test_get_by_id(
    repo: UserInvitationRepository, invitation: UserInvitationEntity
):
    """Test if the invitation can be found with the id."""
    entity = await repo.get_invitation_by_id(invitation.id)
    assert entity.id == invitation.id


async def test_get_by_uuid(
    repo: UserInvitationRepository, invitation: UserInvitationEntity
):
    """Test if the invitation can be found with the unique id."""
    entity = await repo.get_invitation_by_uuid(invitation.uuid)
    assert entity.id == invitation.id


async def test_get_all(repo: UserInvitationRepository):
    """Test get all."""
    invitations = [invitation async for invitation in repo.get_all(repo.create_query())]
    assert len(invitations) > 0, "There should be at least 1 row"


async def test_query_filter_by_email(repo: UserInvitationRepository):
    """Test the filter by email query."""
    query = repo.create_query()
    query.filter_by_email(EmailAddress("ichiro.abe@kwai.com"))
    assert await query.count() > 0, "There should be at least 1 row"


async def test_query_filter_active(repo: UserInvitationRepository):
    """Test the filter active query."""
    query = repo.create_query()
    query.filter_active(LocalTimestamp.create_now())
    assert await query.count() > 0, "There should be at least 1 row"


async def test_delete(repo: UserInvitationRepository, invitation: UserInvitationEntity):
    """Test if the invitation can be deleted."""
    await repo.delete(invitation)

    with pytest.raises(UserInvitationNotFoundException):
        await repo.get_invitation_by_id(invitation.id)
