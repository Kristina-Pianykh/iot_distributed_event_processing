import time
import RPi.GPIO as GPIO
from utils import send_event, set_constants


SENSOR = "sound"
constants = set_constants(SENSOR)

if constants["frequency"] == "rare":
    endpoints = constants["urls"] + constants["local_server_url"]
else:
    endpoints = constants["local_server_url"]

# Define the GPIO pin number for the sound sensor
SOUND_SENSOR_PIN = 17

# Setup GPIO mode and pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)

# Main loop
while True:
    if GPIO.input(SOUND_SENSOR_PIN):
        if constants["frequency"] == "rare":
            send_event(
                urls=endpoints,
                device_id=constants["device_id"],
                sensor=SENSOR,
                sensor_val=1.0,
            )
    time.sleep(constants["interval"])
