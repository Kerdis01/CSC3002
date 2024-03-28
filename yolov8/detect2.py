import csv
import subprocess
import time
import os
from ultralytics import YOLO
import resource_monitor  # Make sure this module exists and is correctly implemented

# Ensure the results directory exists
results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)

# Adjust the CSV file path to be within the results directory
csv_file_path = os.path.join(results_dir, 'detection_metrics.csv')

# Command to launch the camera and create a TCP stream
camera_command = [
    'libcamera-vid',
    '-n',
    '-t', '0',
    '--width', '800',
    '--height', '640',
    '--framerate', '1',
    '--inline',
    '--listen',
    '-o', 'tcp://127.0.0.1:8888'
]

# Launch the camera in a subprocess
subprocess.Popen(camera_command)
time.sleep(5)  # Wait for the camera to be ready

# Prepare CSV file for logging
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write CSV header
    csv_writer.writerow(["Frame", "CPU Usage (%)", "CPU Temperature (C)", "Core Voltage (V)", "Detection Summary", "Detection Pre-process Speed (ms)", "Detection Inference Speed (ms)", "Detection Post Process Speed (ms)"])

    # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')
    stream_url = 'tcp://127.0.0.1:8888'

    results = model(stream_url, stream=True, save=True)
    frame_counter = 0  # Initialize frame counter

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
        csv_writer.writerow([frame_counter, cpu_usage, cpu_temp, core_voltage, detection_summary, preprocess_speed, inference_speed, postprocess_speed])

        # Print the frame and detection summary to the console
        print(f"Frame {frame_counter}: {detection_summary}")

        # Break the loop after processing 10 frames
        if frame_counter == 10:
            break

# Clean up
subprocess.call(['pkill', '-f', 'libcamera-vid'])