import httpx
import json
import time
import yaml

# Set the headers
headers = {
    "Content-Type": "application/json",
}


def send_event(url: str, device_id: str, sensor: str, sensor_val: float) -> None:
    """Send an event to the http server
    and retry if it fails"""
    message = f"{device_id} | {sensor} | {sensor_val} | {int(time.time())}"
    print(message)
    while True:
        try:
            httpx.post(url, headers=headers, data=json.dumps({"Data": message}))
            break
        except Exception as e:
            print(f"Failed to send event: {message} with exception: {e}")
            print("Waiting for the http server to start up...")


def read_config():
    # Open the YAML file and load its content
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        return config
