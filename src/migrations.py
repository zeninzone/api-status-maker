from flask_migrate import Migrate
from app import app, db

migrate = Migrate(app, db)

# This file will be used to run migrations using the following commands:
# flask db init     - Initialize migrations (first time only)
# flask db migrate  - Generate a migration
# flask db upgrade  - Apply migrations
# flask db downgrade - Rollback migrations 