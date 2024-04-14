import csv
import subprocess
import time
import os
from datetime import datetime
from upload_to_s3 import upload_to_s3
from resource_monitor import get_core_voltage, get_cpu_temperature, get_cpu_usage
from ultralytics import YOLO

def run_detection(model_name, model_path, stream_url):
    """
    Run object detection using YOLOv8 model.

    :param model_name: Name of the YOLOv8 model file.
    :param model_path: Directory path where the model file is stored.
    :param stream_url: URL or path for the video stream or file.
    """
    # CSV and AWS Settings
    run_title = datetime.now().strftime('Run_%H%M%S_%d%m%Y_') + model_name
    s3_bucket_name = 'detect-csv-results'
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    csv_file_path = os.path.join(results_dir, f'{run_title}.csv')

    # Launch Camera
    camera_process = subprocess.Popen([
        'libcamera-vid',
        '-n',
        '-t', '0',
        '--width', '800',
        '--height', '640',
        '--framerate', '5',
        '--inline',
        '--listen',
        '-o', stream_url
    ])
    time.sleep(5)  # Wait for the camera to be ready

    # Load the YOLOv8 model
    model = YOLO(os.path.join(model_path, model_name))
    # model.fuse()

    # Prepare CSV file for logging
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Frame", "CPU Usage (%)", "CPU Temperature (C)", "Core Voltage (V)",
                             "Detection Summary", "Detection Inference Speed (ms)", "Confidence Scores", "Average FPS"])

        results = model.track(source=stream_url, stream=True,
                              conf=0.5, iou=0.7, tracker="bytetrack.yaml", show=True)
        frame_counter = 0
        start_time = time.time()

        for result in results:
            frame_counter += 1

            # Calculate average FPS so far
            current_time = time.time()
            elapsed_time = current_time - start_time

            # System metrics
            cpu_usage = get_cpu_usage()
            cpu_temp = get_cpu_temperature()
            core_voltage = get_core_voltage()
            boxes = result.boxes
            class_indices = boxes.cls
            class_names = [result.names[int(cls)] for cls in class_indices]
            detection_summary = f"Objects Detected: {len(result.boxes)}, "+ str(class_names)
            inference_speed = result.speed['inference']
            confidence_scores = result.boxes.conf
            confidence_scores = str(confidence_scores).replace("tensor(", "").replace(")", "")
            avg_fps = frame_counter / elapsed_time if elapsed_time > 0 else 0

            # Write data to CSV, including the formatted Average FPS
            csv_writer.writerow([frame_counter, cpu_usage, cpu_temp, core_voltage,
                             detection_summary, f"{inference_speed:.2f}", confidence_scores, f"{avg_fps:.2f}"])

            if frame_counter > 100:  # Stop after 100 frames
                break

    # Upload the CSV file to AWS S3 and clean up
    upload_to_s3(s3_bucket_name, csv_file_path)
    camera_process.terminate()

if __name__ == "__main__":
    # model_name = 'quantised_yolov8n.pt'
    model_name = 'yolov8n.pt'
    # model_name = 'yolov5s.pt'
    model_path = 'models'
    stream_url = 'tcp://127.0.0.1:8888'
    run_detection(model_name, model_path, stream_url)
