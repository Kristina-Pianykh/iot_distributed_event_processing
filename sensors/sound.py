import RPi.GPIO as GPIO
from utils import send_event
import yaml
import time


# Open the YAML file and load its content
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

sensors = {"sound": 0}
device_id = config["device_id"]
interval = float(config["event"]["sound"]["data_generation_interval"])
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
        send_event()
    # else:
    #     print("No sound detected!")
    time.sleep(interval)

