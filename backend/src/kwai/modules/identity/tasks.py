"""Module that lists all tasks of the identity module."""
from kwai.modules.identity.user_recoveries.user_recovery_events import (
    UserRecoveryCreatedEvent,
)
from kwai.modules.identity.user_recoveries.user_recovery_tasks import (
    email_user_recovery_task,
)

tasks = {UserRecoveryCreatedEvent: email_user_recovery_task}
