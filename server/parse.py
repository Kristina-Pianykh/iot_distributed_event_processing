from typing import Union
from pydantic import BaseModel
import yaml
import httpx
import json
import datetime

def read_config():
    # Open the YAML file and load its content
    with open("../config.yaml", "r") as file:
        config = yaml.safe_load(file)
        return config

class Event(BaseModel):
    device_type: str
    device_id: str
    sensor_id: str
    sensor_value: Union[float, str]
    timestamp: int

    @classmethod
    def from_pi(cls, event_str: str) -> "Event":
        values = event_str.split(" | ")
        device_type = values[0]
        device_id = values[1]
        sensor_id = values[2]
        sensor_value = float(values[3])
        timestamp = int(values[4])
        return cls(
            device_type=device_type,
            device_id=device_id,
            sensor_id=sensor_id,
            sensor_value=sensor_value,
            timestamp=timestamp,
        )

    @classmethod
    def from_watch(cls, sensor_id: str, payload: dict) -> "Event":
        if payload["Value"] in ["", "true", True]:
            value = 1.0
        else:
            value = float(payload["Value"])
        return cls(
            device_type="watch",
            device_id=f"watch_{payload['Origin']}",
            sensor_id=sensor_id.lower(),
            sensor_value=value,
            timestamp=int(payload["Timestamp"]),
        )

# Set the headers
headers = {
    "Content-Type": "application/json",
}


def get_time_in_sec() -> int:
    current_time = datetime.datetime.now()
    return current_time.minute * 60 + current_time.second


def send_event(urls: list[str], device_id: str, sensor: str, sensor_val: float, timestamp: int = get_time_in_sec()) -> None:
    """Send an event to the http server
    and retry if it fails"""
    message = f"pi | {device_id} | {sensor} | {sensor_val} | {timestamp}"
    # print(message)
    for url in urls:
        try:
            httpx.post(url, headers=headers, data=json.dumps(message))
        except Exception as e:
            print(f"Failed to send event: {message} to {url} with exception: {e}")


config = read_config()
watch_events = set([event for watch in config["watches"] for event in config["watches"][watch]["sensors"]])