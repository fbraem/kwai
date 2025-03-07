# Kwai

This repository is (again) a greenfield project: a monorepo containing the source code for the frontend and
the backend of Kwai. Someday, Kwai will be a (sport) club management system.

The system is written following DDD as software development philosophy. Clean code should be the result of following
this philosophy.

## Documentation
The documentation, for backend and frontend, is generated by mkdocs and can be read
[here](https://kwai.readthedocs.io/en/latest/).

## Frontend
The code of the frontend is located in the [frontend](./frontend) folder. It's a monorepo
with applications and packages written in [typescript](https://www.typescriptlang.org/) and
managed by [vite](https://vitejs.dev). The applications use [Vue](https://vuejs.org).

## Backend
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Unlike the [other version](https://github.com/fbraem/kwai-api) which is written in PHP, this backend is written in
Python and uses [FastAPI](https://fastapi.tiangolo.com/) as web framework to provide an API for Kwai.

The code of the [backend](./backend)

At the moment there is no release available yet, but the code is already used by our
judo club: [Judokwai Kemzeke](https://www.judokwaikemzeke.be)
