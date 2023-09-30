from sense_hat import SenseHat
import time
import httpx
import yaml
from parse import read_config


config = read_config()
ip = config["pis"]["pi_3"]["ip"]
url = f"http://{ip}:8000/match"


def flash_rainbow() -> None:
    """
    This function displays a rainbow on the Sense HAT LED matrix."""

    # First check if we are running on a Sense HAT
    try:
        sense = SenseHat()
        # Define RGB values for rainbow colors
        colors = [
            (255, 0, 0),  # Red
            (255, 165, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (75, 0, 130),  # Indigo
            (238, 130, 238),  # Violet
        ]

        # Define the duration (in seconds) for each color
        duration = 0.5

        # Loop through the rainbow colors
        for _ in range(1):
            for color in colors:
                # Set all the LEDs to the current color
                sense.clear(color)

                # Wait for the specified duration
                time.sleep(duration)

                # Clear the LEDs
                sense.clear()

            # Display a blank matrix at the end
            sense.clear()
            time.sleep(0.2)
    except Exception:
        print("No Sense HAT detected, sending to another device")
        httpx.get(url)
