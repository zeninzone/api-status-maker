from flask import Flask, render_template
from schedules import schedulePingApiEndpoint
from flask_apscheduler import APScheduler
from app_config import company_name, api_config, api_ping_frequency_seconds

# Flask App
app = Flask(__name__)
scheduler = APScheduler()


# Routes
@app.route("/")
def hello():
    print(api_config)
    return render_template("index.html", company_name=company_name)


if __name__ == "__main__":
    scheduler.add_job(
        id="Scheduled Task",
        func=schedulePingApiEndpoint,
        trigger="interval",
        seconds=api_ping_frequency_seconds,
    )
    scheduler.start()
    app.run(host="0.0.0.0", port=5001)
