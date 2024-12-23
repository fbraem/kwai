# Welcome to the frontend of kwai.

The frontend consists of several single page applications. [Vue](https://vuejs.org) is used as JavaScript framework.
The frontend code is written with [Typescript](https://www.typescriptlang.org/).

The code is structured as a mono repository. It contains applications and libraries.

## Install

### Prerequisites

Clone the repository to your system.

[npm](https://www.npmjs.com/) is used as packaging and dependency management tool.
Make sure it is available.

Make `frontend` the current directory and use npm to install all dependencies:

`npm install`

[Task](https://taskfile.dev/) can be used as runner and build tool.

### Configuration

The frontend uses a config package.

## Development

A development version of the frontend can be started. Make `frontend` the current directory
and run the `dev_apps` task. This task will build all the packages from the monorepo
and build and serve the applications.

`task dev_apps`

[Vite](https://vitejs.dev/) is the local development server.
Each application will have a vite server.

The FastAPI backend is used to serve all applications.

## Build

To create a production version of the frontend:

`npm run build`

or

`task build_apps`

This will create dist folders in each application.
