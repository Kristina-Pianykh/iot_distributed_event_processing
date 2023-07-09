from sense_hat import SenseHat
import yaml
import time
import json
import httpx


# Open the YAML file and load its content
with open("sensors/config.yaml", "r") as file:
    config = yaml.safe_load(file)

device_id = config["device_id"]
interval = float(config["event"]["joystick"]["data_generation_interval"])
sensor_name = "joystick"
url = config["post_url"]

# Set the headers
headers = {
    "Content-Type": "application/json",
}

# setup sensehat
sense = SenseHat()

while True:
    for event in sense.stick.get_events():
        # Check if the joystick was pressed
        if event.action == "pressed":
            sensor_value = (
                event.direction
            )  # funktioniert nicht solange parser auf double value eingestellt ist

            message = (
                f"{device_id} | {sensor_name} | {sensor_value} | {int(time.time())}"
            )
            print(message)
            httpx.post(url, headers=headers, data=json.dumps({"Data": message}))
        time.sleep(interval)
