from sense_hat import SenseHat
import time
from utils import send_event
import yaml


# Open the YAML file and load its content
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


sensors = {"x": 0, "y": 0, "z": 0}
device_id = config["device_id"]
interval = float(config["event"]["accelerometer"]["data_generation_interval"])
sensor_name = "accelerometer"
url = config["post_url"]

# setup sensehat
sense = SenseHat()

while True:
    acceleration = sense.get_accelerometer_raw()
    # send the dimensions if its value changed
    for key, val in acceleration.items():
        if val != sensors[key]:
            message = f"{device_id} | accelerometer_{key} | {val} | {int(time.time())}"
            print(message)
            send_event(url, message)
            # httpx.post(url, headers=headers, data=json.dumps({"Data": message}))
            sensors[key] = val
        time.sleep(interval)
