"""Package for all database related modules.

ORM (Object-relational mapping) software (like SQLAlchemy) is not used. Instead, the
repository pattern is used. A repository is responsible for saving, creating, querying
and deleting entities. [sql-smith][sql-smith] is used to build queries.

The [DatabaseQuery][kwai.core.db.database_query.DatabaseQuery] class can be used to
implement the Query interface.

[sql-smith]: https://github.com/fbraem/sql-smith
"""
