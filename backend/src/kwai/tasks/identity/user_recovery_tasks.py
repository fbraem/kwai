"""Module that defines entry points for tasks for user recoveries."""
from celery import Task

from kwai.core.events.celery import EventTask


class EmailUserRecoveryTask(EventTask):
    name: str = "identity.user_recovery.email"

    def run(self, *args, **kwargs):
        """A task used to send a mail for a user recovery."""
        print(args)
        print(kwargs)
        return {"test": "Joehoe"}
