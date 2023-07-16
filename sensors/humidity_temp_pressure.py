from sense_hat import SenseHat
import time
import yaml
from utils import send_event, read_config


config = read_config()

SENSOR = "humidity_temp_pressure"
DEVICE_ID = [
    device for device in config["device_id"] if SENSOR in config["device_id"][device]
][0]

sensors = {"humidity": 0, "temp": 0, "pressure": 0}
# device_id = config["device_id"]
interval = float(config["event"][SENSOR]["data_generation_interval"])
url = config["post_url"]

# setup sensehat
sense = SenseHat()

while True:
    fresh = {"humidity": sense.humidity, "temp": sense.temp, "pressure": sense.pressure}
    for key, val in fresh.items():
        if val != sensors[key]:
            # message = f"{DEVICE_ID} | {key} | {val} | {int(time.time())}"
            # print(message)
            send_event(url=url, device_id=DEVICE_ID, sensor=key, sensor_val=val)
            sensors[key] = val
        time.sleep(interval)
