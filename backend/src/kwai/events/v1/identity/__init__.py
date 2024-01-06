"""Module for defining the event router for the identity module."""
from faststream.rabbit import RabbitRouter

from kwai.events.v1.identity.user_invitation_tasks import (
    router as user_invitation_router,
)
from kwai.events.v1.identity.user_recovery_tasks import router as user_recovery_router

router = RabbitRouter(prefix="identity.")
router.include_router(user_invitation_router)
router.include_router(user_recovery_router)
