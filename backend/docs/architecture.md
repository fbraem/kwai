Architecture
============

Kwai tries to follow the [clean architecture](http://cleancoder.com) principles. The [frontend]() is already a
separated layer. The backend code is using the domain driven design (DDD) for modeling the software.

One of the rules of clean architecture is that when you don't own or control something, then keep it on the
outside of your design or wrap it. This means for example, that the domain code isn't allowed to contain FastAPI code
or database related code. The code for the API is on the outside because it's the entry point of a call to the system.
Presenters are used to transform domain objects into JSON:API documents. The repository pattern keeps the
database code on the outside. And interfaces are used to protect the inside from the outside.

![Clean Architecture](/images/clean_architecture.jpg)

The [pendulum](https://pendulum.eustace.io/) library is used for processing dates and timestamps. Because kwai doesn't
own this code, the pendulum code is wrapped into value objects (Timestamp, Date, ...). If the pendulum package is
outdated, we only need to change these value objects.

> This is also the reason why [Pydantic](https://docs.pydantic.dev/latest/) isn't used for entities or value objects.
> Pydantic is great for validation and serialization, but we don't want Pydantic to become a dependency of the kwai
> domain.

Dependency injection containers are only used on the outside. There should not be any magic code in the domain.
So, dependency injection containers can only be used in the API entry code, the CLI entry code, ... From there on,
the dependency should be passed as an argument (and passing it down should be done using an interface).

Actors
======

Who are the actors in our application?

Visitor
-------

A visitor is a person that visits our website. He/She does not have any permissions and is
not known in the system.

Member
------

A member is a person that is a member of the club.

Coach
-----

A coach is a member of the club. A coach can create/view/update/delete trainings. A coach can also registers
participants for a training. When participants are registered, a training can't be deleted anymore.

````mermaid
sequenceDiagram
    actor Coach
    Coach->>Trainings: View
    Coach->>Trainings: Create
    Coach->>Trainings: Update
    Coach->>Trainings: Delete
    Coach->>Trainings: Register participants
````

Admin
-----

An administrator is a person that manages the website.
