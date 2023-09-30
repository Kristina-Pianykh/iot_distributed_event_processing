# setup sensehat
from sense_hat import SenseHat
import shutil
import os

sense_hat_config_path = "/root/.config/sense_hat"


def remove_directory(path):
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                remove_directory(item_path)
        os.rmdir(path)
        print(f"Folder '{path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Folder '{path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


try:
    sense = SenseHat()
except Exception:
    try:
        shutil.rmtree(sense_hat_config_path, ignore_errors=True)
        sense = SenseHat()
    except Exception:
        os.remove(sense_hat_config_path)
        sense = SenseHat()


def get_sense_hat():
    return sense
