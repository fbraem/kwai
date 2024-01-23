"""Module for defining the event router for the identity module."""

from kwai.events.v1.identity.user_invitation_tasks import (
    router as user_invitation_router,
)
from kwai.events.v1.identity.user_recovery_tasks import router as user_recovery_router

router = (
    *user_invitation_router,
    *user_recovery_router,
)
