import random
import time
import os
from utils import send_event, read_config, set_constants


config = read_config()

SENSOR = "sound"
sensors = {"sound": 0}
constants = set_constants()


def simulate_sound_sensor():
    while True:
        send_event(
            urls=constants["urls"],
            device_id=constants["device_id"],
            sensor=SENSOR,
            sensor_val=1.0,
        )
        time.sleep(random.randint(1, 5))


if __name__ == "__main__":
    simulate_sound_sensor()
