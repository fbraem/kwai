"""Module for defining a publisher using faststream.

See: https://faststream.airt.ai/latest/
"""
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange

from kwai.core.events.event import Event
from kwai.core.events.publisher import Publisher


class FaststreamPublisher(Publisher):
    """A publisher using faststream.

    This publisher uses a RabbitMQ broker. The module name is used as exchange name,
    while the event name is the routing key.
    """

    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    def publish(self, event: Event):
        exchange = RabbitExchange(name=event.meta.module, type=ExchangeType.TOPIC)
        self._broker.publish(
            event.data,
            routing_key=event.meta.name,
            exchange=exchange,
        )
