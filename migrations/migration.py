import abc
from tmtvr.db import Database


class BaseMigration(abc.ABC):
    @abc.abstractmethod
    def up(self):
        ...

    @abc.abstractmethod
    def down(self):
        ...


def migrate(db: Database, migrations: list[BaseMigration]):
    for migration in migrations:
        migration.up()
