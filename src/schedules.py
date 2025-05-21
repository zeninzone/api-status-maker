import logging
from datetime import datetime
from .utils import check_api_status
from .app_config import api_config, api_ping_frequency_seconds
from .models import db, ApiStatus, ApiStatusHistory, GlobalSettings

# Store Flask app reference
flask_app = None

def init_scheduler(app):
    global flask_app
    flask_app = app

def execute_and_respond(api_config):
    current_time = datetime.now().strftime("%A, %B %d %H:%M:%S")
    if not flask_app:
        logging.error("Flask app not initialized")
        return
        
    with flask_app.app_context():
        try:
            # Update last check time
            GlobalSettings.set_setting('last_check_time', current_time)
            
            # Clear current status table
            ApiStatus.query.delete()
            
            for conf in api_config:
                api_name = conf["api_name"]
                api_url = conf["api_url"]
                api_response = check_api_status(api_url)
                
                # Create new status entry
                status = ApiStatus(
                    api_name=api_name,
                    api_url=api_url,
                    status_code=api_response["status_code"],
                    status_text=api_response["api_status_text"],
                    message=api_response["message"],
                    response_time=api_response["response_time"]
                )
                
                # Create history entry
                history = ApiStatusHistory(
                    api_name=api_name,
                    api_url=api_url,
                    status_code=api_response["status_code"],
                    status_text=api_response["api_status_text"],
                    message=api_response["message"],
                    response_time=api_response["response_time"]
                )
                
                db.session.add(status)
                db.session.add(history)
            
            db.session.commit()
            logging.info("Successfully updated API statuses")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating API statuses: {str(e)}")


def schedulePingApiEndpoint():
    print(f"This job runs every {api_ping_frequency_seconds} seconds")
    execute_and_respond(api_config)


def read_last_call_time():
    if not flask_app:
        return datetime.now().strftime("%A, %B %d %H:%M:%S")
        
    with flask_app.app_context():
        last_check = GlobalSettings.get_setting('last_check_time')
        if not last_check:
            current_time = datetime.now().strftime("%A, %B %d %H:%M:%S")
            GlobalSettings.set_setting('last_check_time', current_time)
            return current_time
        return last_check
