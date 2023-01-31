# Kwai

This repository is (again) a greenfield project: a monorepo containing the source code for the frontend and
the backend of Kwai. Someday, Kwai will be a (sport) club management system.

The system is written following DDD as software development philosophy. Clean code should be the result of following 
this philosophy.

## Frontend
The frontend consists of several single page applications. [Vue](https://vuejs.org) is used as JavaScript framework. 
Currently, the source code is still located in a separate repository: [kwai-vite](https://github.com/fbraem/kwai-vite). 
Eventually the code will be moved to this repository.

## Backend
Unlike the [other version](https://github.com/fbraem/kwai-api) which is written in PHP, this backend is written in 
Python and uses [FastAPI](https://fastapi.tiangolo.com/) as web framework to provide an API for Kwai.

For more information about the backend: [README.md](./backend)

At the moment there is no release available yet.

## Acknowledgments

Thanks to [JetBrains](https://www.jetbrains.com/), Kwai is developed using [PyCharm](https://www.jetbrains.com/pycharm/).
