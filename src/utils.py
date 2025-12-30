import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_notification(to_email, subject, body):
    """Send email notification for status changes"""
    # Note: Configure these with your email settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your-email@gmail.com"  # Configure this
    sender_password = "your-app-password"  # Configure this

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"Failed to send notification: {str(e)}")
        return False


def check_api_status(api_url, previous_status=None):
    start_time = time.time()
    try:
        response = requests.get(api_url, timeout=30)
        response_time = time.time() - start_time

        # Check if the status code indicates a successful request (2xx)
        if response.status_code // 100 == 2:
            message = f"The API is up. Status message: {response.reason}"
            api_status_text = "healthy"
        else:
            message = f"The API is down. Status code: {response.status_code}, Reason: {response.reason}"
            api_status_text = "unhealthy"

        status_data = {
            "status_code": response.status_code,
            "message": message,
            "api_status_text": api_status_text,
            "response_time": float(round(response_time, 3)),
        }

    except requests.ConnectionError:
        message = "Failed to connect to the API. It may be down or unreachable."
        api_status_text = "unhealthy"
        status_data = {
            "status_code": 500,
            "message": message,
            "api_status_text": api_status_text,
            "response_time": 0.0,
        }
    except requests.Timeout:
        message = "API request timed out after 30 seconds"
        api_status_text = "timeout"
        status_data = {
            "status_code": 504,
            "message": message,
            "api_status_text": api_status_text,
            "response_time": 30.0,
        }

    return status_data


def get_theme_css(theme="light"):
    """Return CSS variables for different themes"""
    themes = {
        "light": {
            "bg-color": "#ffffff",
            "text-color": "#000000",
            "primary-color": "#6dc77a",
            "secondary-color": "#f7f8fa",
            "accent-color": "#4a90e2",
        },
        "dark": {
            "bg-color": "#1a1a1a",
            "text-color": "#ffffff",
            "primary-color": "#6dc77a",
            "secondary-color": "#2d2d2d",
            "accent-color": "#4a90e2",
        },
        "blue": {
            "bg-color": "#f0f8ff",
            "text-color": "#000000",
            "primary-color": "#4a90e2",
            "secondary-color": "#e6f3ff",
            "accent-color": "#2d73c9",
        },
        "purple": {
            "bg-color": "#f8f0ff",
            "text-color": "#000000",
            "primary-color": "#9b59b6",
            "secondary-color": "#f3e6ff",
            "accent-color": "#8e44ad",
        },
    }

    return themes.get(theme, themes["light"])
