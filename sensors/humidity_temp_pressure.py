import time
import yaml
from utils import send_event, set_constants
from sensehat import sense


# config = read_config()

SENSOR = "humidity_temp_pressure"
sensors = {"humidity": 0, "temp": 0, "pressure": 0}
# device_id = config["device_id"]
# interval = float(config["event"][SENSOR]["data_generation_interval"])
constants = set_constants(SENSOR)

# # setup sensehat
# sense = SenseHat()

while True:
    fresh = {"humidity": sense.humidity, "temp": sense.temp, "pressure": sense.pressure}
    for key, val in fresh.items():
        if val != sensors[key]:
            # message = f"{DEVICE_ID} | {key} | {val} | {int(time.time())}"
            # print(message)
            send_event(
                urls=constants["urls"],
                device_id=constants["device_id"],
                sensor=key,
                sensor_val=val,
            )
            sensors[key] = val
        time.sleep(constants["interval"])
