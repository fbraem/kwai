"""Module for testing the user invitation tasks."""
from kwai.core.domain.value_objects.unique_id import UniqueId
from kwai.core.events.publisher import Publisher
from kwai.modules.identity.user_invitations.user_invitation_events import (
    UserInvitationCreatedEvent,
)


def test_user_invitation_created(publisher: Publisher):
    """Test user invitation created event."""
    publisher.publish(UserInvitationCreatedEvent(uuid=str(UniqueId.generate())))
