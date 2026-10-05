import os
import random
import time

import requests

API_URL = os.getenv("API_URL", "http://api:5000/humidity")
DEVICE_ID = os.getenv("DEVICE_ID", "sensor-01")

while True:
    value = round(random.uniform(30, 80), 2)
    payload = {"device_id": DEVICE_ID, "humidity": value}
    try:
        r = requests.post(API_URL, json=payload, timeout=5)
        print(f"Sent {payload} -> {r.status_code}", flush=True)
    except requests.exceptions.RequestException as e:
        print(f"Backend unavailable, will retry: {e}", flush=True)
    time.sleep(3)