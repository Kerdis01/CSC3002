import csv
import subprocess
import time
import os
from datetime import datetime
from upload_to_s3 import upload_to_s3
import resource_monitor as resource_monitor
from ultralytics import YOLO

# Model Settings
model_name = 'quantised_yolov8n.pt'
model_path = 'models'

# CSV and AWS Settings
run_title = datetime.now().strftime('Run_%H%M%S_%d%m%Y_') + model_name
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
camera_process = subprocess.Popen(camera_command)
time.sleep(5)  # Wait for the camera to be ready

# Load the YOLOv8 model
model = YOLO(os.path.join(model_path, model_name))
model.fuse()

# Prepare CSV file for logging
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write CSV header to include Average FPS
    csv_writer.writerow(["Frame", "CPU Usage (%)", "CPU Temperature (C)", "Core Voltage (V)",
                         "Detection Summary", "Detection Inference Speed (ms)", "Average FPS"])
    
    results = model.track(source=stream_url, stream=True, conf=0.5, iou=0.7, tracker="bytetrack.yaml", show=True)
    frame_counter = 0
    start_time = time.time()  # Start time for FPS calculation

    for result in results:
        frame_counter += 1

        # Calculate average FPS so far
        current_time = time.time()
        elapsed_time = current_time - start_time

        # System metrics
        cpu_usage = resource_monitor.get_cpu_usage()
        cpu_temp = resource_monitor.get_cpu_temperature()
        core_voltage = resource_monitor.get_core_voltage()
        detection_summary = f"Objects Detected: {len(result.boxes)}"
        inference_speed = result.speed['inference']
        avg_fps = frame_counter / elapsed_time if elapsed_time > 0 else 0

        # Write data to CSV, including the formatted Average FPS
        csv_writer.writerow([frame_counter, cpu_usage, cpu_temp, core_voltage,
                             detection_summary, f"{inference_speed:.2f}", f"{avg_fps:.2f}"])

        print(f"Frame {frame_counter}: {detection_summary}, Avg FPS: {avg_fps:.2f}")

        if frame_counter > 100:  # Stop after 100 frames
            break

# Upload the CSV file to AWS S3
upload_to_s3(s3_bucket_name, csv_file_path)
# Clean up
camera_process.terminate()
