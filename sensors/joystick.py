import time
from utils import send_event, set_constants
from sensehat import get_sense_hat


# config = read_config()
sense = get_sense_hat()
SENSOR = "joystick"
constants = set_constants(SENSOR)

if constants["frequency"] == "rare":
    endpoints = constants["urls"] + constants["local_server_url"]
else:
    endpoints = constants["local_server_url"]


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
            else:
                sensor_value = 0.0
            # sensor_value = (
            #     event.direction
            # )  # funktioniert nicht solange parser auf double value eingestellt ist

            # message = (
            #     f"{device_id} | {sensor_name} | {sensor_value} | {int(time.time())}"
            # )
            # print(message)
            if constants["frequency"] == "rare":
                send_event(
                    urls=endpoints,
                    device_id=constants["device_id"],
                    sensor=SENSOR,
                    sensor_val=sensor_value,
                )
            # httpx.post(url, headers=headers, data=json.dumps({"Data": message}))
        time.sleep(constants["interval"])
