from flask import render_template, jsonify, request
from .schedules import read_last_call_time, schedulePingApiEndpoint, init_scheduler
from .app_config import title, description, environment, logo, api_ping_frequency_seconds, mask_api_urls
from .models import ApiStatus, ApiStatusHistory, UserPreferences, GlobalSettings
from .utils import get_theme_css
from . import create_app, db, scheduler
import logging
from configparser import ConfigParser

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create Flask app
app = create_app()

# Read default theme from config
config = ConfigParser()
config.read("./config/config.ini")
default_theme = config.get("global_config", "default_theme")

# Create database tables and initialize default settings
with app.app_context():
    db.create_all()

    # Initialize default theme if not exists
    if not GlobalSettings.query.filter_by(key="theme").first():
        theme_setting = GlobalSettings(key="theme", value=default_theme)
        db.session.add(theme_setting)
        db.session.commit()

# Initialize scheduler with app context
init_scheduler(app)

# Configure scheduler job
scheduler.add_job(
    id="API Status Check",
    func=schedulePingApiEndpoint,
    trigger="interval",
    seconds=api_ping_frequency_seconds,
)


# Routes
@app.route("/")
def home():
    current_statuses = ApiStatus.query.all()
    user_prefs = UserPreferences.query.first()

    # Get theme from database or use default
    current_theme = GlobalSettings.get_setting("theme", default_theme)

    # Enhance status data with additional information
    enhanced_statuses = []
    for status in current_statuses:
        status_data = status.serialize
        # Add uptime percentage
        status_data["uptime_percentage"] = ApiStatusHistory.get_uptime_percentage(
            status.api_name
        )
        # Add response time stats
        status_data["response_time_stats"] = ApiStatusHistory.get_response_time_stats(
            status.api_name
        )
        # Add historical data for graphs
        status_data["history_data"] = ApiStatusHistory.get_history_data(status.api_name)
        enhanced_statuses.append(status_data)

    healthy_count = sum(1 for s in enhanced_statuses if s.get("api_last_status_code") == 200)
    unhealthy_count = len(enhanced_statuses) - healthy_count

    return render_template(
        "index.html",
        title=title,
        description=description,
        environment=environment,
        logo=logo,
        api_responses=enhanced_statuses,
        api_ping_frequency_seconds=api_ping_frequency_seconds,
        resp_time=read_last_call_time(),
        theme=current_theme,
        notifications_enabled=user_prefs.notification_enabled if user_prefs else False,
        mask_api_urls=mask_api_urls,
        healthy_count=healthy_count,
        unhealthy_count=unhealthy_count,
    )


@app.route("/change_theme", methods=["POST"])
def change_theme():
    data = request.json
    new_theme = data.get("theme", default_theme)

    with app.app_context():
        # Update theme in GlobalSettings
        GlobalSettings.set_setting("theme", new_theme)

    return jsonify({"status": "success", "theme": new_theme})


@app.route("/toggle_notifications", methods=["POST"])
def toggle_notifications():
    data = request.json
    enabled = data.get("enabled", True)

    with app.app_context():
        prefs = UserPreferences.query.first()
        if not prefs:
            prefs = UserPreferences(notification_enabled=enabled)
            db.session.add(prefs)
        else:
            prefs.notification_enabled = enabled
        db.session.commit()

    return jsonify({"status": "success"})


@app.route("/api/status")
def get_status():
    """API endpoint for fetching current status data"""
    current_statuses = ApiStatus.query.all()
    enhanced_statuses = []
    for status in current_statuses:
        status_data = status.serialize
        status_data["uptime_percentage"] = ApiStatusHistory.get_uptime_percentage(
            status.api_name
        )
        status_data["response_time_stats"] = ApiStatusHistory.get_response_time_stats(
            status.api_name
        )
        status_data["history_data"] = ApiStatusHistory.get_history_data(status.api_name)
        enhanced_statuses.append(status_data)

    healthy_count = sum(1 for s in enhanced_statuses if s.get("api_last_status_code") == 200)
    unhealthy_count = len(enhanced_statuses) - healthy_count

    return jsonify(
        {
            "statuses": enhanced_statuses,
            "last_check": read_last_call_time(),
            "healthy_count": healthy_count,
            "unhealthy_count": unhealthy_count,
        }
    )


if __name__ == "__main__":
    # Configure scheduler
    scheduler.init_app(app)
    scheduler.start()

    # Run the app
    app.run(host="0.0.0.0", port=5001)
