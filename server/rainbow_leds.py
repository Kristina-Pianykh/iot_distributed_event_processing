from sense_hat import SenseHat
import time
import httpx
import yaml


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

ip = config["device"]["pi_3"]["ip"]
url = f"http://{ip}/post"

def flash_rainbow() -> None:
    """
    This function displays a rainbow on the Sense HAT LED matrix."""

    # First check if we are running on a Sense HAT
    try:
        sense = SenseHat()
    except OSError:
        print("No Sense HAT detected, sending to another device")
        httpx.post(url)

    # Define RGB values for rainbow colors
    colors = [
        (255, 0, 0),     # Red
        (255, 165, 0),   # Orange
        (255, 255, 0),   # Yellow
        (0, 255, 0),     # Green
        (0, 0, 255),     # Blue
        (75, 0, 130),    # Indigo
        (238, 130, 238)  # Violet
    ]

    # Define the duration (in seconds) for each color
    duration = 0.5

    # Loop through the rainbow colors
    for _ in range(5):
        for color in colors:
            # Set all the LEDs to the current color
            sense.clear(color)
            
            # Wait for the specified duration
            time.sleep(duration)
            
            # Clear the LEDs
            sense.clear()

        # Display a blank matrix at the end
        sense.clear()
        time.sleep(0.5)
