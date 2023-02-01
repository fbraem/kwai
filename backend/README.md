# Kwai Backend

The kwai backend provides an api for kwai. All server side code is written
with Python. The web framework used is [FastAPI](https://fastapi.tiangolo.com/).

## Prereqs
 
+ Clone the repository to your system.
+ [Poetry](https://python-poetry.org/) is used as Python packaging and
dependency management tool. Make sure it is available.
+ Use Poetry to install all dependencies.

## Configuration

A `kwai.dist.toml` file is available to create the configuration file.
Copy this file and update it with your configuration. Make sure not to add
this file to version control.

Set the full path of the configuration file in the environment variable `KWAI_SETTINGS_FILE`.  

To avoid abuse, make sure that this file is located in a private folder and not
available from the internet.

## Database

Kwai needs a database. Migration files are available in the folder migrations.
[Dbmate](https://github.com/amacneil/dbmate) is used as migration tool.

````shell
dbmate -d "./migrations" --url protocol://user:password@host:port/database migrate
````

> Note: only "up" migrations are provided. Create a backup of the database before 
> running the migrations. Although dbmate can run "down" migrations, they are not
> used because these are hard to test and can generate more problems than they solve.

## Project Structure

### migrations

This folder contains all database migrations.

### src

This folder contains all Python code.

### templates

This folder contains all templates used by kwai.

### vagrant

This folder contains the scripts to set up a vagrant environment. This vagrant setup will create
+ A MySQL database.
+ dbmate for running migrations.
+ A RabbitMQ broker for pub/sub.
+ Mailcatcher to test sending emails.

Use the `kwai.dist.yaml` file to create `kwai.yaml`. This file must contain settings.

## Code

### api

### core

### modules

#### identity

## Test

## Deploy

