import json
import os
import requests
from datetime import datetime, timezone

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=37.5&longitude=-122.0&current_weather=true"
MEMORY_FILE = "memory.json"
TIME_LIMIT_HOURS = 24


# -------------------------
# Memory handling
# -------------------------

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "start_time": None,
            "temperature_history": []
        }

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# -------------------------
# API call
# -------------------------

def fetch_weather():
    response = requests.get(API_URL)
    data = response.json()

    # Open-Meteo format: current_weather.temperature
    temp = data["current_weather"]["temperature"]
    return temp


# -------------------------
# Time logic
# -------------------------

def get_current_time():
    return datetime.now(timezone.utc)


def parse_time(t):
    return datetime.fromisoformat(t.replace("Z", "+00:00"))


def hours_elapsed(start_time_str):
    start = parse_time(start_time_str)
    now = get_current_time()
    delta = now - start
    return delta.total_seconds() / 3600


# -------------------------
# Agent loop
# -------------------------

def run_agent():
    memory = load_memory()

    now_iso = get_current_time().isoformat()

    # Initialize start time once
    if memory["start_time"] is None:
        memory["start_time"] = now_iso
        save_memory(memory)

    # Check elapsed time
    elapsed = hours_elapsed(memory["start_time"])

    if elapsed >= TIME_LIMIT_HOURS:
        print(f"Stopping agent: {elapsed:.2f} hours elapsed (limit = 24 hours).")
        return

    # Fetch weather
    temperature = fetch_weather()

    # Append to history
    memory["temperature_history"].append({
        "time": now_iso,
        "temperature": temperature
    })

    save_memory(memory)

    print(f"Recorded temperature: {temperature}°C at {now_iso}")
    print(f"Elapsed time: {elapsed:.2f} hours")


if __name__ == "__main__":
    run_agent()