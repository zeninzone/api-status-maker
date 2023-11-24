import logging
from utils import check_api_status

def schedulePingApiEndpoint():
    print("This test runs every 3 seconds")
    check_api_status("https://youtube.com/health")
    logging.info('This is an info message')