import os
from pathlib import Path
import time
from picamera2 import Picamera2
import argparse

parser = argparse.ArgumentParser(description="Capture images using Picamera2.")
parser.add_argument("--time_interval", type=float, default=1.0, help="Time interval between captures in seconds.")
parser.add_argument("--num_images", type=int, default=10, help="Number of images to capture.")
parser.add_argument("--resolution", type=str, default="480x640", help="Output resolution in WxH format.")
args = parser.parse_args()

# Extract resolution from argument
width, height = map(int, args.resolution.split('x'))

RES_OUT = (width, height)
DRIVE_ID = os.listdir("/media/kin")[0] # Bad practice but acceptable for small project
VOLUME_PATH = f"/media/kin/{DRIVE_ID}/shared/ML/picam/data" # Bad practice but acceptable for small project
Path(VOLUME_PATH).mkdir(parents=True, exist_ok=True)

# Initialize Picamera2
picam2 = Picamera2()

config = picam2.create_still_configuration(lores=None)
picam2.configure(config)

# Start the camera once
picam2.start()
time.sleep(1)  # Give the camera time to warm up

# Capture images in a loop without stopping the camera
for i in range(args.num_images):
    # Capture the image
    image = picam2.capture_image("main")

    # Apply transformations
    image = image.rotate(-90, expand=True)
    image = image.resize(RES_OUT)

    image_path = f"{VOLUME_PATH}/{int(time.time())}.jpg"
    image.save(image_path)

    # Sleep to control the interval between captures
    time.sleep(args.time_interval)

# Stop the camera after the loop is done
picam2.stop()
