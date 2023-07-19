import RPi.GPIO as GPIO
from utils import send_event, read_config, set_constants
import yaml
import time


config = read_config()

SENSOR = "sound"
sensors = {"sound": 0}
# device_id = config["device_id"]
interval = float(config["event"][SENSOR]["data_generation_interval"])
constants = set_constants()

# Define the GPIO pin number for the sound sensor
SOUND_SENSOR_PIN = 17

# Setup GPIO mode and pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)

# Main loop
while True:
    if GPIO.input(SOUND_SENSOR_PIN):
        print("Sound detected!")
        # message = f"{DEVICE_ID} | {SENSOR} | 1 | {int(time.time())}"
        send_event(
            urls=constants["urls"],
            device_id=constants["device_id"],
            sensor=SENSOR,
            sensor_val=1.0,
        )
    # else:
    #     print("No sound detected!")
    time.sleep(interval)
