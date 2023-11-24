import requests


def check_api_status(api_url):
    try:
        response = requests.get(api_url)

        # Check if the status code indicates a successful request (2xx)
        if response.status_code // 100 == 2:
            message = f"The API is up. Status message: {response.reason}"
        else:
            message = f"The API is down. Status code: {response.status_code}, Reason: {response.reason}"

        return {"status_code": response.status_code, "message": message}

    except requests.ConnectionError:
        message = "Failed to connect to the API. It may be down or unreachable."
        return {
            "status_code": 500,
            "message": message,
        }
