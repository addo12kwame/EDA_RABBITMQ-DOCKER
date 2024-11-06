from main import app, db
from flask_migrate import Migrate
from flask_script import Manager, Command
import os

migrate = Migrate(app, db)
manager = Manager(app)

# Define a custom command to initialize migrations
class InitDB(Command):
    "Initializes the migration repository"
    def run(self):
        if not os.path.exists('migrations'):
            Migrate(app, db).init()
        else:
            print("Migrations folder already exists")

# Define a custom command to create a new migration
class MigrateDB(Command):
    "Creates a new migration based on model changes"
    def run(self):
        Migrate(app, db).migrate()

# Define a custom command to apply migrations to the database
class UpgradeDB(Command):
    "Applies migrations to the database"
    def run(self):
        Migrate(app, db).upgrade()

# Add the custom commands to the manager
manager.add_command('db_init', InitDB())
manager.add_command('db_migrate', MigrateDB())
manager.add_command('db_upgrade', UpgradeDB())

if __name__ == "__main__":
    manager.run()
