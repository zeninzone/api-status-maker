from flask import Flask, render_template
from schedules import read_last_call_time, schedulePingApiEndpoint
from flask_apscheduler import APScheduler
from app_config import title, description, api_ping_frequency_seconds, result

# Flask App
app = Flask(__name__)
scheduler = APScheduler()


# Routes
@app.route("/")
def home():
    return render_template(
        "index.html",
        title=title,
        description=description,
        api_responses=result,
        api_ping_frequency_seconds=api_ping_frequency_seconds,
        resp_time=read_last_call_time(),
    )


if __name__ == "__main__":
    scheduler.add_job(
        id="Scheduled Task",
        func=schedulePingApiEndpoint,
        trigger="interval",
        seconds=api_ping_frequency_seconds,
    )
    scheduler.start()
    app.run(host="0.0.0.0", port=5001)
