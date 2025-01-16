"""Module for defining a publisher using FastStream."""

from faststream.redis import RedisBroker
from loguru import logger

from kwai.core.events.event import Event
from kwai.core.events.publisher import Publisher


class FastStreamPublisher(Publisher):
    """A publisher using FastStream."""

    def __init__(self, broker: RedisBroker):
        self._broker = broker

    async def publish(self, event: Event):
        logger.info(f"Publishing event {event.meta.name} to {event.meta.module}")
        await self._broker.publish(
            event.data,
            stream=event.meta.full_name,
        )
