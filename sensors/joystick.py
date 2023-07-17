from sense_hat import SenseHat
import yaml
import time
from utils import send_event, read_config


config = read_config()

SENSOR = "joystick"
DEVICE_ID = [
    device_id
    for device_id, device_info in config["device"].items()
    if SENSOR in device_info.get("sensors", [])
][0]

# device_id = config["device_id"]
interval = float(config["event"]["joystick"]["data_generation_interval"])
# sensor_name = "joystick"
url = config["post_url"]


# setup sensehat
sense = SenseHat()

while True:
    for event in sense.stick.get_events():
        # Check if the joystick was pressed
        if event.action == "pressed":
            if event.direction == "up":
                sensor_value = 1.0
            elif event.direction == "down":
                sensor_value = -1.0
            elif event.direction == "left":
                sensor_value = -0.1
            elif event.direction == "right":
                sensor_value = 0.1
            # sensor_value = (
            #     event.direction
            # )  # funktioniert nicht solange parser auf double value eingestellt ist

            # message = (
            #     f"{device_id} | {sensor_name} | {sensor_value} | {int(time.time())}"
            # )
            # print(message)
            send_event(
                url=url, device_id=DEVICE_ID, sensor=SENSOR, sensor_val=sensor_value
            )
            # httpx.post(url, headers=headers, data=json.dumps({"Data": message}))
        time.sleep(interval)
