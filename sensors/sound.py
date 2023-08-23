import time
import RPi.GPIO as GPIO
from utils import send_event, set_constants


SENSOR = "sound"
# config = read_config()
# interval = float(config["event"]["sound"]["data_generation_interval"])
constants = set_constants(SENSOR)

# Define the GPIO pin number for the sound sensor
SOUND_SENSOR_PIN = 17

# Setup GPIO mode and pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_SENSOR_PIN, GPIO.IN)

# Main loop
while True:
    if GPIO.input(SOUND_SENSOR_PIN):
        send_event(
            urls=constants["urls"],
            device_id=constants["device_id"],
            sensor=SENSOR,
            sensor_val=1.0,
        )
    time.sleep(constants["interval"])
