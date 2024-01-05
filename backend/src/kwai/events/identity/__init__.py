"""Module for defining the message router for the identity module."""
from faststream.rabbit import RabbitRouter

from kwai.events.identity.user_invitation_tasks import router as user_invitation_router

router = RabbitRouter(prefix="identity.")
router.include_router(user_invitation_router)
