from sense_hat import SenseHat
import time
from utils import send_event, read_config
import yaml

config = read_config()

SENSOR = "accelerometer"
DEVICE_ID = [
    device_id
    for device_id, device_info in config["device"].items()
    if SENSOR in device_info.get("sensors", [])
][0]

sensors = {"x": 0, "y": 0, "z": 0}
# device_id = config["device_id"]
interval = float(config["event"][SENSOR]["data_generation_interval"])
url = config["post_url"]

# setup sensehat
sense = SenseHat()

while True:
    acceleration = sense.get_accelerometer_raw()
    # send the dimensions if its value changed
    for key, val in acceleration.items():
        if val != sensors[key]:
            # message = f"{DEVICE_ID} | accelerometer_{key} | {val} | {int(time.time())}"
            # print(message)
            send_event(
                url=url,
                device_id=DEVICE_ID,
                sensor=f"accelerometer_{key}",
                sensor_val=val,
            )
            # httpx.post(url, headers=headers, data=json.dumps({"Data": message}))
            sensors[key] = val
        time.sleep(interval)
