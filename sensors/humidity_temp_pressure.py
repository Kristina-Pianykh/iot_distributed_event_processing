import time
from utils import send_event, set_constants
from sensehat import get_sense_hat


sense = get_sense_hat()


# config = read_config()

SENSOR = "humidity_temp_pressure"
sensors = {"humidity": 0, "temp": 0, "pressure": 0}
constants = set_constants(SENSOR)

if constants["frequency"] == "rare":
    endpoints = constants["urls"] + constants["local_server_url"]
else:
    endpoints = constants["local_server_url"]

while True:
    fresh = {"humidity": sense.humidity, "temp": sense.temp, "pressure": sense.pressure}
    for key, val in fresh.items():
        if val != sensors[key]:
            # message = f"{DEVICE_ID} | {key} | {val} | {int(time.time())}"
            # print(message)
            send_event(
                urls=endpoints,
                device_id=constants["device_id"],
                sensor=key,
                sensor_val=round(val, 3),
            )
            sensors[key] = val
        time.sleep(constants["interval"])
