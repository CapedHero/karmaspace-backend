from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test.testcases import TestCase


class TestMigrations(TestCase):
    """
    Django TestCase for testing migrations, especially migration logic.

    Based on:
    + https://stackoverflow.com/questions/44003620/how-do-i-run-tests-against-a-django-data-migration
    + https://www.caktusgroup.com/blog/2016/02/02/writing-unit-tests-django-migrations/
    """

    app = None
    migrate_from = None
    migrate_to = None

    def setUp(self):
        assert self.app and self.migrate_from and self.migrate_to, (
            "TestMigrations TestCase requires defining class attributes "
            "'app', 'migrate_from', and 'migrate_to'."
        )

        self.migrate_from = [(self.app, self.migrate_from)]
        self.migrate_to = [(self.app, self.migrate_to)]
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(self.migrate_from).apps

        # Reverse to the original migration.
        executor.migrate(self.migrate_from)

        # Set database to the desired state for testing.
        self.setUpBeforeMigration(old_apps)

        # Run the migration to test.
        executor = MigrationExecutor(connection)

        # Reload.
        executor.loader.build_graph()
        executor.migrate(self.migrate_to)
        self.apps = executor.loader.project_state(self.migrate_to).apps

    def setUpBeforeMigration(self, apps):
        pass
