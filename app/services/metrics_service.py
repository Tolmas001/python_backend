import json
import os

FILE = "storage/metrics.json"
DEFAULT_DATA = {
    "total_requests": 0,
    "positive": 0,
    "negative": 0,
    "general": 0
}


def ensure_file():
    os.makedirs(os.path.dirname(FILE), exist_ok=True)
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump(DEFAULT_DATA, f, indent=4)


def update_metrics(sentiment):
    ensure_file()
    try:
        with open(FILE) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = DEFAULT_DATA.copy()

    data["total_requests"] += 1

    if sentiment == "positive":
        data["positive"] += 1
    elif sentiment == "negative":
        data["negative"] += 1
    else:
        data["general"] += 1

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_metrics():
    ensure_file()
    try:
        with open(FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return DEFAULT_DATA.copy()
