"""Module that lists all tasks of the identity module."""
from kwai.modules.identity.user_recoveries.user_recovery_tasks import (
    EmailUserRecoveryTask,
)

tasks = [EmailUserRecoveryTask]
