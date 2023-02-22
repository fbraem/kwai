"""Module for testing UserInvitationDbRepository."""
import pytest

from kwai.core.db.database import Database
from kwai.core.domain.value_objects.email_address import EmailAddress
from kwai.core.domain.value_objects.name import Name
from kwai.modules.identity.user_invitations.user_invitation import UserInvitationEntity
from kwai.modules.identity.user_invitations.user_invitation_db_repository import (
    InvitationDbRepository,
)
from kwai.modules.identity.user_invitations.user_invitation_repository import (
    UserInvitationRepository,
    UserInvitationNotFoundException,
)
from kwai.modules.identity.users.user import UserEntity

pytestmark = pytest.mark.integration

# pylint: disable=redefined-outer-name


@pytest.fixture(scope="module")
def repo(database: Database) -> UserInvitationRepository:
    """Fixture for creating the invitation repository."""
    return InvitationDbRepository(database)


@pytest.fixture(scope="module")
def invitation(
    repo: UserInvitationRepository, user: UserEntity
) -> UserInvitationEntity:
    """Fixture for an invitation."""
    invitation = UserInvitationEntity(
        email=EmailAddress("ichiro.abe@kwai.com"),
        name=Name(first_name="Ichiro", last_name="Abe"),
        remark="Created with pytest",
        user=user,
    )
    return repo.create(invitation)


def test_create(invitation: UserInvitationEntity):
    """Test if the invitation was created."""
    assert not invitation.id.is_empty(), "There should be an invitation created"


def test_get_by_id(repo: UserInvitationRepository, invitation: UserInvitationEntity):
    """Test if the invitation can be found with the id."""
    entity = repo.get_invitation_by_id(invitation.id)
    assert entity.id == invitation.id


def test_get_by_uuid(repo: UserInvitationRepository, invitation: UserInvitationEntity):
    """Test if the invitation can be found with the unique id."""
    entity = repo.get_invitation_by_uuid(invitation.uuid)
    assert entity.id == invitation.id


def test_get_all(repo: UserInvitationRepository):
    assert (
        len(list(repo.get_all(repo.create_query()))) > 0
    ), "There should be at least 1 row"


def test_query_filter_by_email(repo: UserInvitationRepository):
    query = repo.create_query()
    query.filter_by_email(EmailAddress("ichiro.abe@kwai.com"))
    assert len(list(repo.get_all(query))) > 0, "There should be at least 1 row"


def test_delete(repo: UserInvitationRepository, invitation: UserInvitationEntity):
    """Test if the invitation can be deleted."""
    repo.delete(invitation)

    with pytest.raises(UserInvitationNotFoundException):
        repo.get_invitation_by_id(invitation.id)
