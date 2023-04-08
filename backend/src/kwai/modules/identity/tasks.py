"""Module that lists all tasks of the identity module."""
from kwai.modules.identity.user_invitations.user_invitation_events import (
    UserInvitationCreatedEvent,
)
from kwai.modules.identity.user_invitations.user_invitation_tasks import (
    email_user_invitation_task,
)
from kwai.modules.identity.user_recoveries.user_recovery_events import (
    UserRecoveryCreatedEvent,
)
from kwai.modules.identity.user_recoveries.user_recovery_tasks import (
    email_user_recovery_task,
)

tasks = {
    UserRecoveryCreatedEvent: email_user_recovery_task,
    UserInvitationCreatedEvent: email_user_invitation_task,
}
