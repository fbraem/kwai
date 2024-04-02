"""Module that implements a unit of work pattern."""

from kwai.core.db.database import Database


class UnitOfWork:
    """A unit of work implementation."""

    def __init__(self, database: Database):
        self._database = database

    async def __aenter__(self):
        """Enter the unit of work."""
        await self._database.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the unit of work.

        When an exception occurred, the transaction will be rollbacked.
        """
        if exc_type:
            await self._database.rollback()
        else:
            await self._database.commit()
