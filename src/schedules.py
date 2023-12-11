import json
import logging
from datetime import datetime
from utils import check_api_status
from app_config import api_config, api_ping_frequency_seconds


def execute_and_respond(api_config):
    write_last_call_time()
    response = list()
    for conf in api_config:
        api_name = conf["api_name"]
        api_url = conf["api_url"]
        api_response = check_api_status(api_url)
        response.append(
            {
                "api_name": api_name,
                "api_url": api_url,
                "api_last_status_code": api_response["status_code"],
                "api_status_text": api_response["api_status_text"],
                "api_last_msg": api_response["message"],
            }
        )
    return response


def schedulePingApiEndpoint():
    print(f"This job runs every {api_ping_frequency_seconds} seconds")
    result = execute_and_respond(api_config)
    with open("./result.json", "w") as f:
        json.dump(result, f)
    logging.info("This is an info message from schedulePingApiEndpoint")


def read_last_call_time():
    with open("last_call_record.txt", "r") as file:
        resp = file.read().strip()
    print(resp)
    return resp


def write_last_call_time():
    with open("last_call_record.txt", "w+") as f:
        f.write(datetime.now().strftime("%A, %B %d %H:%M:%S"))
    return True
