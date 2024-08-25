import time
import requests

def safeRequest(url, maxRetries=8, delaySeconds=12):
    for attempt in range(maxRetries):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        if attempt < maxRetries - 1:
            time.sleep(delaySeconds)
    return None
