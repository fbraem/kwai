# Deploy kwai backend

This page will describe how you can deploy the backend of kwai.

## Step 1: Clone

First you need to get the latest version. The repository is a monorepo.
This means the backend code and the frontend code are in the same repository.
We only need the backend here:

````shell
git clone --no-checkout https://codeberg.org/zumuta/kwai.git
cd kwai
git sparse-checkout init --cone
git sparse-checkout set backend
git checkout
````

> When sparse-checkout is not available, you can safely remove the frontend directory.

## Step 2: Python Environment

Kwai needs a Python environment. [Poetry](https://python-poetry.org/) is used as Python packaging and
dependency management tool. Make sure it is available.

````shell
cd backend/src
poetry install
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

## Step 4: Migration

When there are database changes required, a migration must run before
starting the backend.

> [dbmate](https://github.com/amacneil/dbmate) is used for database migrations. Make sure it is available.

````shell
cd backend/migrations
dbmate -d . -u "<database_uri>" up
````

## Step 4: Frontend

Build the frontend :

````shell
cd frontend
npm run build
````

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

## Step 5: Run

To start the backend application use the following command:

````shell
cd backend/src
poetry run python -m kwai.api
````

This python script will start an uvicorn server. The host
and port arguments can be used to configure this server.
