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

def print_progress_bar(iteration, total, prefix='', length=50, fill='█', print_end="\r"):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    records_info = f"{iteration}/{total}"
    print(f'\r{prefix} |{bar}| {percent}% Complete ({records_info})', end=print_end)
