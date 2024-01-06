"""Package for events.

Subscribe to an event to process the event. One event can have multiple subscribers.
Just use a different queue for each subscriber of the same event. Subscribers are
triggered by the FastStream application.

A use case is responsible for publishing the events to a broker.

Events are dataclasses.
"""
