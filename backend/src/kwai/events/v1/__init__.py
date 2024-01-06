"""Package for handling v1 events.

A version is used to handle changes of the event data. When a structure of an event
changes, a new version should be created when there are still old events to process.
"""
from faststream.rabbit import RabbitRouter

from kwai.events.v1.identity import router as identity_router

router = RabbitRouter(prefix="v1.")
router.include_router(identity_router)
