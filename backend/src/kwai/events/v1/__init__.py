"""Package for handling v1 events.

A version is used to handle changes of the event data. When a structure of an event
changes, a new version should be created when there are still old events to process.
"""

from kwai.events.v1.identity import router as identity_router


router = ()
router += identity_router
