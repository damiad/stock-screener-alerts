import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Add logic when to actually send alert and when not to...
def send_pushover_notification(message):
    pushover_token = os.getenv("pushover_token")
    pushover_user_key = os.getenv("pushover_user_key")
    pushover_url = "https://api.pushover.net/1/messages.json"

    pushover_data = {
        "token": pushover_token,
        "user": pushover_user_key,
        "message": message,
    }
    requests.post(pushover_url, data=pushover_data)
