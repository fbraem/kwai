"""Module for defining a publisher using faststream.

See: https://faststream.airt.ai/latest/
"""
from faststream.redis import RedisBroker
from loguru import logger

from kwai.core.events.event import Event
from kwai.core.events.publisher import Publisher


class FaststreamPublisher(Publisher):
    """A publisher using faststream.

    This publisher uses a RabbitMQ broker. The module name is used as exchange name,
    while the event name is the routing key.
    """

    def __init__(self, broker: RedisBroker):
        self._broker = broker

    async def publish(self, event: Event):
        logger.info(
            f"Publishing event {event.meta.name} to exchange {event.meta.module}"
        )
        await self._broker.publish(
            event.data,
            stream=f"{event.meta.version}.{event.meta.module}.{event.meta.name}",
        )
