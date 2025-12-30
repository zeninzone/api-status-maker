from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
import os

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
scheduler = APScheduler()


def create_app():
    app = Flask(__name__)

    # Configure SQLite database
    # Create database directory if it doesn't exist
    db_dir = os.path.join(os.path.dirname(__file__), "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "api_status.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize and start scheduler
    scheduler.init_app(app)
    scheduler.start()

    return app
