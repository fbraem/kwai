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

> Note: we only provide "up" migrations. Create a backup of the database before 
> running the migrations.

## structure

### api

### core

### modules

#### identity

## Test

## Deploy

