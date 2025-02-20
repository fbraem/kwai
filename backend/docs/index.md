# Welcome to the backend of kwai.

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![coverage](../coverage/coverage.svg)](../coverage/index.html)

This is the backend for the KWAI sports club management system. This system
contains a [JSON:API](https://jsonapi.org/) REST API, a CLI and an event bus.

All server side code is written with Python using [FastAPI](https://fastapi.tiangolo.com/) for the REST API
and [Typer](https://typer.tiangolo.com/) for the CLI. Currently, the event bus is not in use yet.

!!! note
    The frontend is also served by FastAPI.

## Develop

### Prerequisites

Clone the repository to your system.

[Poetry](https://python-poetry.org/) is used as Python packaging and
dependency management tool. Make sure it is available.

Use Poetry to install all the dependencies: Make `backend` the current directory
and run:

`poetry install`

This will only install the modules required to run KWAI, for developing add `dev` and `docs` dependencies:

`poetry install --with dev,docs`

### Configuration

A `kwai.dist.toml` file is available to create the configuration file.
Copy this file and update it with your configuration. Make sure not to add
this file to version control.

Set the full path of the configuration file in the environment variable `KWAI_SETTINGS_FILE`.

To avoid abuse, make sure that this file is located in a private folder and not
available from the internet.

### Database

KWAI needs a database. Migration files are available in the folder migrations.
[Dbmate](https://github.com/amacneil/dbmate) is used as migration tool.

```console
dbmate -d "./migrations" --url protocol://user:password@host:port/database up
```

!!! note
    Create a .env file to avoid entering the dbmate arguments over and over again.
    See [Command line options](https://github.com/amacneil/dbmate?tab=readme-ov-file#command-line-options).

!!! note
    only "up" migrations are provided. Create a backup of the database before
    running the migrations. Although dbmate can run "down" migrations, they are not
    used because these are hard to test and can generate more problems than they solve.

### Redis
kwai uses [Redis](https://redis.io) for handling events. When an event is published, it will be put on a stream.
Each event will have its own stream. Make sure the settings for redis are set in the configuration file.

A separate process is used to handle the events: `kwai_bus`.

### CLI
A CLI program can be used to test and interrogate the system. See [CLI](cli.md) for more information.

### Docker

To make testing easier, a docker compose file is provided to set up a container with the required
infrastructure. This will install and create the following containers:

+ A MySQL database.
+ redis for events.
+ Mailcatcher for testing emails.

Use a .env file for setting the password for mysql (KWAI_DB_PASSWORD) and redis (KWAI_REDIS_PASSWORD).

> Don't add `.env` to version control!

### Tools

The backend is written in Python. The following tools are used to develop kwai:
+ [Poetry](https://python-poetry.org/) for managing dependencies.
+ [Black](https://black.readthedocs.io/en/stable/) for formatting the code,
+ [ruff](https://docs.astral.sh/ruff/) for linter.
+ [pytest](https://docs.pytest.org) for testing the code.

There are pre-commit hooks defined for formatting and linting the code. Use
Poetry to create the pre-commit hooks:

> Use the backend folder as working directory for the poetry commands.

````
poetry run pre-commit install
````

There are several github actions defined:

+ backend_test: will run all pytest test when code is pushed in backend/src.
+ generate_docs: will generate this documentation.
+ mirror: will copy the repository to codeberg.
+ ruff: will check the code.

### Project structure

The kwai API code in the repository is located in the `backend` folder.

#### docs

This folder contains all files for creating this documentation site.

#### migrations

This folder contains the database migrations.
[Dbmate](https://github.com/amacneil/dbmate) is used as migration tool.

#### src

This folder contains the Python code. The system is written following DDD as software development philosophy.
Clean code should be the result of following this philosophy. The folder `kwai` contains the
program code, `tests` contains the [pytest](https://pytest.org) code for testing the program code.
