import subprocess
import time
import os
from ultralytics import YOLO


def run_detection(model_name, model_path, stream_url):
    """
    Run object detection using YOLOv8 model.

    :param model_name: Name of the YOLOv8 model file.
    :param model_path: Directory path where the model file is stored.
    :param stream_url: URL or path for the video stream or file.
    """
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
    time.sleep(5)

    model = YOLO(os.path.join(model_path, model_name))
    model.fuse()

    frame_counter = 0
    start_time = time.time()
    try:
        results = model.track(source=stream_url, stream=True, conf=0.5, iou=0.7, tracker="bytetrack.yaml", show=True)
        for result in results:
            frame_counter += 1
            current_time = time.time()
            elapsed_time = current_time - start_time
            avg_fps = frame_counter / elapsed_time if elapsed_time > 0 else 0
            detection_summary = f"Objects Detected: {len(result.boxes)}, Average FPS: {avg_fps:.2f}"
            print(detection_summary)
    except KeyboardInterrupt:
        print("Interrupt received, stopping...")
    finally:
        print("Terminating camera process...")
        camera_process.terminate()


if __name__ == "__main__":
    model_name = 'quantised_yolov8n.pt'
    model_path = 'models'
    stream_url = 'tcp://127.0.0.1:8888'
    run_detection(model_name, model_path, stream_url)
