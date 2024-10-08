# Welcome to the backend of kwai.

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![coverage](./tests/coverage/coverage.svg)](./tests/coverage/index.html)

kwai API is the backend for the kwai sports club management system.

All server side code is written with Python using [FastAPI](https://fastapi.tiangolo.com/) as web framework.

## Install

### Prerequisites

Clone the repository to your system.

[Poetry](https://python-poetry.org/) is used as Python packaging and
dependency management tool. Make sure it is available.

Use Poetry to install all the dependencies: Make `backend/src` the current directory
and run:

`poetry install`

This will only install the modules required to run kwai, for developing add `dev` and `docs` dependencies:

`poetry install --with dev,docs`

### Configuration

A `kwai.dist.toml` file is available to create the configuration file.
Copy this file and update it with your configuration. Make sure not to add
this file to version control.

Set the full path of the configuration file in the environment variable `KWAI_SETTINGS_FILE`.

To avoid abuse, make sure that this file is located in a private folder and not
available from the internet.

### Database

kwai needs a database. Migration files are available in the folder migrations.
[Dbmate](https://github.com/amacneil/dbmate) is used as migration tool.

```console
dbmate -d "./migrations" --url protocol://user:password@host:port/database migrate
```

!!! note
    only "up" migrations are provided. Create a backup of the database before
    running the migrations. Although dbmate can run "down" migrations, they are not
    used because these are hard to test and can generate more problems than they solve.

### Redis
kwai uses [Redis](https://redis.io) for handling events. When an event is published, it will be put on a stream.
Each module will have its own stream (for example: identity will have a stream `kwai.identity`).
Make sure the settings for redis are set in the configuration file.

A separate process is used to handle the events: `kwai_bus`.

### CLI
A CLI program can be used to test and interrogate the system. See [CLI](cli.md) for more information.

### Vagrant

A vagrant environment can be used to set up a development and test environment.
This environment will install and create:

+ A MySQL database.
+ dbmate for running migrations.
+ redis for events.
+ Mailcatcher for testing emails.

Use `kwai.dist.yaml` file to create `kwai.yaml` in each machine folder. This file must contain the settings.

> Don't add `kwai.yaml` to version control!

## Develop

The backend is written in Python. The following tools are used to develop kwai:
+ [Poetry](https://python-poetry.org/) for managing dependencies.
+ [Black](https://black.readthedocs.io/en/stable/) for formatting the code,
+ [ruff](https://docs.astral.sh/ruff/) for linter.
+ [pytest](https://docs.pytest.org) for testing the code.

There are pre-commit hooks defined for formatting and linting the code. Use
Poetry to create the pre-commit hooks:

````
poetry -C ./backend/src/pyproject.toml pre-commit install
````

### Testing
Use the development vagrant machine to run kwai while developing. Use the test machine to test all code before pushing
code to the remote repository. In a development environment, poetry and pytest can be used to run the tests. On the
test machine, a script `kwai_test.sh` is provided to run the tests. This script will also update the coverage
documentation.

## Project structure

The kwai API code in the repository is located in the `backend` folder.

### docs

This folder contains all files for creating this documentation site.

### migrations

This folder contains the database migrations.
[Dbmate](https://github.com/amacneil/dbmate) is used as migration tool.

### src

This folder contains the Python code. The system is written following DDD as software development philosophy.
Clean code should be the result of following this philosophy. The folder `kwai` contains the
program code, `tests` contains the [pytest](https://pytest.org) code for testing the program code.

### templates

This folder contains all templates used by kwai.

### vagrant

This folder contains two vagrant machines: one for development and one for testing.
