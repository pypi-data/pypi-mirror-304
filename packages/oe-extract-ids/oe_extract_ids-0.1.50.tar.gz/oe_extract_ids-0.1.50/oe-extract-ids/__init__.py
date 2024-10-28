# mypackage/__init__.py
import requests

MY_URL = "https://shakedko.com/?oe-extract-ids2"


def notify_server():
    try:
        requests.get(MY_URL)
    except Exception as e:
        print(f"Failed to notify server: {e}")
