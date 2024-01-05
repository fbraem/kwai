"""Module for defining the faststream application."""
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from kwai.core.settings import get_settings
from kwai.events.identity import router

settings = get_settings()
broker = RabbitBroker(
    host=settings.rabbitmq.host,
    port=settings.rabbitmq.port,
    login=settings.rabbitmq.user,
    password=settings.rabbitmq.password,
    virtualhost=settings.rabbitmq.vhost,
)
broker.include_router(router)
app = FastStream(broker)
