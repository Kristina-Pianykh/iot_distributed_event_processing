import time
from utils import send_event, set_constants
from sensehat import get_sense_hat

sense = get_sense_hat()
# config = read_config()

SENSOR = "accelerometer"

sensors = {"x": 0, "y": 0, "z": 0}
# device_id = config["device_id"]
# interval = float(config["event"][SENSOR]["data_generation_interval"])
constants = set_constants(SENSOR)

# # setup sensehat
# sense = SenseHat()

while True:
    acceleration = sense.get_accelerometer_raw()
    # send the dimensions if its value changed
    for key, val in acceleration.items():
        if val != sensors[key]:
            # message = f"{DEVICE_ID} | accelerometer_{key} | {val} | {int(time.time())}"
            # print(message)
            send_event(
                urls=constants["urls"],
                device_id=constants["device_id"],
                sensor=f"accelerometer_{key}",
                sensor_val=val,
            )
            # httpx.post(url, headers=headers, data=json.dumps({"Data": message}))
            sensors[key] = val
        time.sleep(constants["interval"])
