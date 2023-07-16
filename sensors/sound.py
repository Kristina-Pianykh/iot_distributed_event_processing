import RPi.GPIO as GPIO
from utils import send_event, read_config
import yaml
import time


config = read_config()

SENSOR = "sound"
DEVICE_ID = [
    device for device in config["device_id"] if SENSOR in config["device_id"][device]
][0]


sensors = {"sound": 0}
# device_id = config["device_id"]
interval = float(config["event"][SENSOR]["data_generation_interval"])
url = config["post_url"]

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
        send_event(url=url, device_id=DEVICE_ID, sensor=SENSOR, sensor_val=1.0)
    # else:
    #     print("No sound detected!")
    time.sleep(interval)
