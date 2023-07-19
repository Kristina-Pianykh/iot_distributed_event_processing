# setup sensehat
from sense_hat import SenseHat

try:
    sense = SenseHat()
except OSError:
    pass
