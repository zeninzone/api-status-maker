import json
from configparser import ConfigParser

# Read global and api config file
global_config = ConfigParser()
global_config.read("./config/config.ini")

# Read global configurations
title = global_config.get("global_config", "title")
description = global_config.get("global_config", "description")
notification_email_address = global_config.get(
    "global_config", "notification_email_address"
)
api_ping_frequency_seconds = global_config.getint(
    "global_config", "api_ping_frequency_seconds"
)
try:
    mask_api_urls = global_config.getboolean("global_config", "mask_api_urls")
except:
    mask_api_urls = False  # Default to False if not specified

# Read API configurations
api_config = []
for section in global_config.sections():
    if section.startswith("api_"):
        api_config.append(
            {
                "api_name": global_config.get(section, "api_name"),
                "api_url": global_config.get(section, "api_url"),
            }
        )

# Read results
try:
    with open("./result.json", "r") as result_data:
        result = json.load(result_data)
except (FileNotFoundError, json.JSONDecodeError):
    result = []

# https://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file
