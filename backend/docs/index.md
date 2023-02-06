# Welcome to kwai API

[![pylint](https://github.com/fbraem/kwai/actions/workflows/pylint.yaml/badge.svg)](https://github.com/fbraem/kwai/actions/workflows/pylint.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

kwai API is the backend for the kwai sports club management system.

All server side code is written with Python using [FastAPI](https://fastapi.tiangolo.com/) as web framework.

## Install

### Prerequisites
 
+ Clone the repository to your system.
+ [Poetry](https://python-poetry.org/) is used as Python packaging and
dependency management tool. Make sure it is available.
+ Use Poetry to install all dependencies: Make `backend/src` the current directory 
and run `poetry install`

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

### Vagrant

A vagrant environment can be used to set up a test environment.
This environment will install and create:

+ A MySQL database.
+ dbmate for running migrations.
+ A RabbitMQ broker for pub/sub.
+ Mailcatcher for testing emails.

Use the `kwai.dist.yaml` file to create `kwai.yaml`. This file must contain settings.

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

This folder contains all files for setting up a test environment.
