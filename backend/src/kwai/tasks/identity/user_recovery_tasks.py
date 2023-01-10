"""Module that defines entry points for tasks for user recoveries."""
from celery import Task


class EmailUserRecoveryTask(Task):
    name: str = "identity.user_recovery.email"
    queue: str = "identity"

    def run(self, *args, **kwargs):
        """A task used to send a mail for a user recovery."""
        print(args)
        print(kwargs)
        return {"test": "Joehoe"}
