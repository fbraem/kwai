"""Package for events.

Events are implemented as actors for Dramatiq. Use EventActor as base class for an
actor. EventActor will set up logging information and provides the actor the dependency
container.

Note: Don't pass the container to the business code, get the dependencies from
the container and pass them through.
"""
