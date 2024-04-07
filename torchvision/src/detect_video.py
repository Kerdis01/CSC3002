import cv2
import torch
import argparse
import time
import os
from datetime import datetime
import csv
import subprocess
from detect_utils import predict, draw_boxes
from model import get_model
import resource_monitor
from upload_to_s3 import upload_to_s3

# Construct the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--threshold', default=0.5,
                    type=float, help='detection threshold')
args = vars(parser.parse_args())

# Define the computation device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = get_model(device)

# CSV and AWS Settings
model_name = 'ssdlite320_mobilenet_v3_large'  # Change to your actual model name
run_title = datetime.now().strftime('Run_%H%M%S_%d%m%Y_') + model_name
s3_bucket_name = 'detect-csv-results'
results_dir = 'results'
os.makedirs(results_dir, exist_ok=True)
csv_file_path = os.path.join(results_dir, f'{run_title}.csv')

# Prepare CSV file for logging
with open(csv_file_path, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Frame", "CPU Usage (%)", "CPU Temperature (C)", 
                         "Core Voltage (V)", "Detection Summary", "Inference Time (ms)", "Confidence Scores",
                         "Avg FPS"])

# Camera stream settings and launch command
stream_url = 'tcp://127.0.0.1:8888'
camera_command = [
    'libcamera-vid', '-n', '-t', '0', '--width', '800', '--height', '640', '--framerate', '5', '--inline', '--listen', '-o', stream_url
]
camera_process = subprocess.Popen(camera_command)
print("Starting camera stream...")
time.sleep(5)  # Wait for the camera to be ready

# Open the CSV file again for appending data
with open(csv_file_path, mode='a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Connect to the camera stream with OpenCV
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print('Error while trying to read video stream. Please check the camera setup.')
        camera_process.terminate()
        exit()

    frame_count = 0
    total_fps = 0
    should_exit = False

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame_start_time = time.time()

                # Perform object detection on the frame
                with torch.no_grad():
                    start_time = time.time()
                    boxes, classes, labels, scores = predict(
                        frame, model, device, args['threshold'])
                # Draw bounding boxes and labels on the frame
                image = draw_boxes(boxes, classes, labels, scores, frame)

                # Calculate FPS
                end_time = time.time()
                fps = 1 / (end_time - frame_start_time)
                total_fps += fps
                frame_count += 1
                if frame_count >= 100:
                    should_exit = True

                # System metrics
                cpu_usage = resource_monitor.get_cpu_usage()
                cpu_temp = resource_monitor.get_cpu_temperature()
                cpu_voltage = resource_monitor.get_core_voltage()
                inference_time = f"{((time.time() - start_time) * 1000):.2f}" # (ms)
                detection_summary = f"Objects Detected: {len(classes)}, "+str(classes)
                confidence_scores = ", ".join([f"{score:.2f}" for score in scores])
                fps = f"{fps:.2f}"

                # Log data to CSV
                csv_writer.writerow(
                    [frame_count, cpu_usage, cpu_temp, cpu_voltage, detection_summary, inference_time, confidence_scores, fps])
                csvfile.flush()

                # Display the frame
                cv2.imshow('Video Stream', image)

                if cv2.waitKey(1) & 0xFF == ord('q') or should_exit:
                    break
            else:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        camera_process.terminate()  # Gracefully terminate the camera process
        avg_fps = total_fps / frame_count if frame_count else 0
        print(f"Average FPS: {avg_fps:.3f}")

        # Upload the CSV file to AWS S3
        upload_to_s3(s3_bucket_name, csv_file_path)
