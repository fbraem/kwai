# Deploy kwai backend

This page will describe how you can deploy the backend of kwai.

## Step 1: Build

First you need to get the latest version. The repository is a monorepo.
This means the backend code and the frontend code are in the same repository.
We only need the backend. Set up the [development environment](./index.md) for kwai
and build the wheel file.

````shell
cd backend
poetry build
````

This command creates a dist folder where you find two files: a tar.gz with the source code and a .whl file
that can used to install kwai.
Transfer the .whl file to your host.

## Step 2: Python Environment

Kwai needs a Python environment. It is recommended to create a separate environment for kwai.
Run the following command on your host:

````shell
mkdir backend
python3 -m venv .venv
source .venv/bin/activate
pip install kwai-x.x.x-py3-none-any.whl
````

## Step 3: Configuration

Kwai needs a configuration file. When this is the first time, we need to
create it.

````shell
cd backend
cp kwai.dist.toml .kwai.toml
````

Use an editor to change the configuration. Set the environment
variable `KWAI_SETTINGS_FILE` with the full path of this configuration file.

## Step 4: Templates

kwai requires jinja2 templates. Copy the templates to a folder on the server
and update the `path` setting in the `template` section of the configuration file.

## Step 5: Migration

When there are database changes required, a migration must run before
starting the backend. Copy the migrations folder to your server and use dbmate to upgrade.

> [dbmate](https://github.com/amacneil/dbmate) is used for database migrations. Make sure it is available.

````shell
cd <your_folder_on_the_server>/migrations
dbmate -d . -u "<database_uri>" up
````

## Step 6: Frontend

The frontend is also served by the FastAPI backend.

To build the frontend you need [Node](https://nodejs.org/en).

````shell
cd frontend
npm install
npm run build
````

!!! Note
    You can also use [Task](https://taskfile.dev/) to build the frontend. Run the following
    command from the kwai root folder:
    `task frontend:build`

This will result in a folder `dist` in all the frontend applications.
FastAPI will be used to render the frontend. Add all applications to the `.kwai.toml` configuration file:

````toml
[frontend]
path = "/home/kwai/frontend"
root_app = "portal"

[frontend.apps]

[frontend.apps.portal]
base="/apps/portal"
entries="/src/index.ts"
````

In this example there should be a `/home/kwai/frontend/apps/portal/dist` folder that contains the result of the
build command.

## Step 7: Run

To start the backend application use the following command:

````shell
cd backend

source .venv/bin/activate
python -m kwai
````

This python script will start an uvicorn server. The host
and port arguments can be used to configure this server.
