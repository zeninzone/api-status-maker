import json
from configparser import ConfigParser

# Read global and api config file

global_config = ConfigParser()
global_config.read("../config/config.ini")

with open("../config/api_config.json", "r") as f:
    api_config = json.load(f)

company_name = global_config.get("global_config", "company_name")
notification_email_address = global_config.get(
    "global_config", "notification_email_address"
)
api_ping_frequency_seconds = global_config.getint(
    "global_config", "api_ping_frequency_seconds"
)


# https://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file
