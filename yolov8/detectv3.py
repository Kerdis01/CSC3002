import csv
import subprocess
import time
import os
from ultralytics import YOLO
from datetime import datetime
from upload_to_s3 import upload_to_s3
import resource_monitor

# Model Settings 
# model_name = 'best-t5.pt' # Model with forward pass and new weights from backpropagation
model_name = 'yolov8n.pt'

# CSV and AWS Settings
run_title = datetime.now().strftime('Run_%H%M%S_%d%m%Y_')+model_name
s3_bucket_name = 'detect-csv-results'  
results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)
csv_file_path = os.path.join(results_dir, f'{run_title}.csv')

# Camera Settings
stream_url = 'tcp://127.0.0.1:8888'
camera_command = [
    'libcamera-vid',
    '-n',
    '-t', '0',
    '--width', '800',
    '--height', '640',
    '--framerate', '5',
    '--inline',
    '--listen',
    '-o', stream_url
]

# Launch Camera
subprocess.Popen(camera_command)
time.sleep(5)  # Wait for the camera to be ready

# Load the YOLOv8 model
model = YOLO(model_name)
# model.half()
model.fuse()
# model.eval()  # Apply quantization
# metrics = model.val(data='coco8.yaml',
                            #    imgsz=640,
                            #    batch=16,
                            #    conf=0.25,
                            #    iou=0.6,
                            #    device='cpu')
# precision = metrics.box.maps

# Prepare CSV file for logging
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write CSV header
    csv_writer.writerow(["Frame", "CPU Usage (%)", "CPU Temperature (C)", "Core Voltage (V)", "Detection Summary",
                        "Detection Pre-process Speed (ms)", "Detection Inference Speed (ms)", "Detection Post Process Speed (ms)", "Precision", "Recall", "F1 Score"])
    # Use source=0 for a USB webcam
    results = model.track(source=stream_url, stream=True,
                          conf=0.5, iou=0.7, tracker="bytetrack.yaml", show=True)
    frame_counter = 0  # Initialize frame counter

    # IMPORTANT: ADD ACCURACY
    for result in results:
        frame_counter += 1

        # Fetch system metrics
        cpu_usage = resource_monitor.get_cpu_usage()
        cpu_temp = resource_monitor.get_cpu_temperature()
        core_voltage = resource_monitor.get_core_voltage()

        # Simplified detection summary for CSV
        detection_summary = f"Objects Detected: {len(result.boxes)}"
        preprocess_speed = result.speed['preprocess']
        inference_speed = result.speed['inference']
        postprocess_speed = result.speed['postprocess']

        # Write data to CSV
        csv_writer.writerow([frame_counter, cpu_usage, cpu_temp, core_voltage,
                            detection_summary, preprocess_speed, inference_speed, postprocess_speed])

        # Print the frame and detection summary to the console
        print(f"Frame {frame_counter}: {detection_summary}")

        # Break the loop after processing 10 frames
        if frame_counter > 10:
            break

upload_to_s3(s3_bucket_name, csv_file_path)
# Clean up
subprocess.call(['pkill', '-f', 'libcamera-vid'])
