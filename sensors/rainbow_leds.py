from sense_hat import SenseHat
import time


def rainbow_leds() -> None:
    """
    This function displays a rainbow on the Sense HAT LED matrix."""
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
    while True:
        for color in colors:
            # Set all the LEDs to the current color
            sense.clear(color)

            # Wait for the specified duration
            time.sleep(duration)

            # Clear the LEDs
            sense.clear()

        # Display a blank matrix at the end
        sense.clear()
        time.sleep(1)
