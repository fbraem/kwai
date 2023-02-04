.. kwai documentation master file, created by
   sphinx-quickstart on Sat Feb  4 12:55:00 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Kwai backend
============

The kwai backend provides an api for kwai. All server side code is written with Python.
FastAPI_ is used as web framework.

Prerequisites
-------------
+ Clone the repository to your system.
+ Poetry_ is used as Python packaging and dependency management tool. Make sure it is available.
+ Use Poetry to install all dependencies.

Configuration
-------------
A ``kwai.dist.toml`` file is available to create the configuration file.
Copy this file and update it with your configuration. Make sure not to add
this file to version control.

Set the full path of the configuration file in the environment variable ``KWAI_SETTINGS_FILE``.

To avoid abuse, make sure that this file is located in a private folder and not
available from the internet.

Database
````````
Kwai needs a database. Migration files are available in the folder migrations.
dbmate_ is used as migration tool.

.. code-block:: sh

   dbmate -d "./migrations" --url protocol://user:password@host:port/database migrate
..

    **Note:** only "up" migrations are provided. Create a backup of the database before
    running the migrations. Although dbmate can run "down" migrations, they are not
    used because these are hard to test and can generate more problems than they solve.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   Kwai package <kwai/modules>
   Tests <tests/modules>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _FastAPI: https://fastapi.tiangolo.com
.. _Poetry: https://python-poetry.org
.. _dbmate: https://github.com/amacneil/dbmate
