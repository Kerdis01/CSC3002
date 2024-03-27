import subprocess
import time
import resource_monitor
from threading import Thread
from ultralytics import YOLO

# Command to launch the camera and create a TCP stream
camera_command = [
    'libcamera-vid',
    '-n',
    '-t', '0',
    '--width', '800',
    '--height', '640',
    '--framerate', '15',
    '--inline',
    '--listen',
    '-o', 'tcp://127.0.0.1:8888'
]

# Launch the camera in a subprocess
subprocess.Popen(camera_command)
time.sleep(5)

# Start the metrics logging in a separate thread to run it in parallel with your main script
metrics_thread = Thread(target=resource_monitor.log_system_metrics_to_csv, args=(5,), daemon=True)
metrics_thread.start()

#Configuring this will significantly improve inference times. Needs optimised.
inference_args=[]

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
stream_url = ('tcp://127.0.0.1:8888')

results = model(stream_url, stream=True)
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    