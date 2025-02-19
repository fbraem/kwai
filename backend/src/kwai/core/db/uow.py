"""Module that implements a unit of work pattern."""

from kwai.core.db.database import Database


class UnitOfWork:
    """A unit of work implementation."""

    def __init__(self, database: Database, *, always_commit: bool = False):
        """Initialize the unit of work.

        When always_commit is True, the unit of work will always be committed, even
        when an exception occurred.
        """
        self._database = database
        self._always_commit = always_commit

    async def __aenter__(self):
        """Enter the unit of work."""
        await self._database.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the unit of work.

        When an exception occurred and always_commit is False, the transaction will
        be rollbacked.
        """
        if self._always_commit:
            await self._database.commit()
            return

        if exc_type:
            await self._database.rollback()
        else:
            await self._database.commit()
