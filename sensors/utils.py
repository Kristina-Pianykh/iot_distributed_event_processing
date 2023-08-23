from typing import Any
import httpx
import os
import json
import yaml
import datetime


# Set the headers
headers = {
    "Content-Type": "application/json",
}


def get_time_in_sec() -> int:
    current_time = datetime.datetime.now()
    return current_time.minute * 60 + current_time.second


def send_event(urls: list[str], device_id: str, sensor: str, sensor_val: float) -> None:
    """Send an event to the http server
    and retry if it fails"""
    message = f"pi | {device_id} | {sensor} | {sensor_val} | {get_time_in_sec()}"
    # print(message)
    for url in urls:
        try:
            httpx.post(url, headers=headers, data=json.dumps(message))
        except Exception as e:
            print(f"Failed to send event: {message} to {url} with exception: {e}")


def read_config():
    # Open the YAML file and load its content
    with open("../config.yaml", "r") as file:
        config = yaml.safe_load(file)
        return config


# Some useful constants defined per device
# retuen a dict with device_id, ips, urls for devices other than yourself
def set_constants(sensor_id: str) -> dict[str, Any]:
    config = read_config()
    device_id = os.getenv("DEVICE_ID")
    ips = [
        device_info["ip"]
        for device, device_info in config["device"].items()
        if device != device_id
    ]
    urls = [f"{config['post_url']}"] + [f"http://{ip}:8000" for ip in ips]
    return {
        "device_id": device_id,
        "ips": ips,
        "urls": urls,
        "interval": float(
            config["event"].get(sensor_id, {}).get("data_generation_interval", 0)
        ),
    }
