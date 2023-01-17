"""Module that defines a message bus using dramatiq."""
import dramatiq
from dramatiq import Broker, group, GenericActor, Message, Actor, actor

from kwai.core.events import Bus, Event


class DramatiqBus(Bus):
    """A message bus implemented with dramatiq."""

    def __init__(self, broker: Broker | None = None):
        self._broker = broker or dramatiq.get_broker()
        self._events = {}

    def publish(self, event: Event):
        """Publish the event.

        The queue name is based on the first part of the event name.
        """
        queue = event.meta.name.split(".")[0]
        self._broker.enqueue(
            Message(
                queue_name=queue,
                actor_name=event.meta.name,
                args=(event.data,),
                kwargs={},
                options={},
            )
        )

    def subscribe(self, event: type[Event], task: type[GenericActor] | str | Actor):
        """Subscribe an actor to an event.

        The queue name is based on the first part of the event name.
        """
        if event.meta.name not in self._events:
            self._events[event.meta.name] = []

        queue = event.meta.name.split(".")[0]

        if isinstance(task, GenericActor):
            task.queue_name = queue
            self._broker.declare_actor(task)
            self._events[event.meta.name].append(task)
        elif isinstance(task, Actor):
            task.queue_name = queue
            self._events[event.meta.name].append(task)
        else:
            task_actor = self._broker.get_actor(task)
            if task_actor:
                task_actor.queue_name = queue
                self._events[event.meta.name].append(task_actor)

        @actor(actor_name=event.meta.name, queue_name=queue)
        def act(data):
            """An actor for sending the event to all actors that are subscribed."""
            group([t.message(data) for t in self._events[event.meta.name]]).run()
