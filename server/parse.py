from typing import Union
from pydantic import BaseModel
import yaml

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
        device_id = values[0]
        sensor_id = values[1]
        sensor_value = float(values[2])
        timestamp = int(values[3])
        return cls(
            device_id=device_id,
            sensor_id=sensor_id,
            sensor_value=sensor_value,
            timestamp=timestamp,
        )

    @classmethod
    def from_watch(cls, events_payload: dict) -> "Event":
        for event in watch_events:
            if event in events_payload:
                return cls(
                    device_type="watch",
                    device_id="watch",
                    sensor_id=event,
                    sensor_value=float(events_payload[event]),
                    timestamp=events_payload["timestamp"],  # TODO: check formatting
                )


config = read_config()
watch_events = set([event for event in config["watches"]["sensors"]])