import argparse
import subprocess
import time
import os
from ultralytics import YOLO

def run_detection(model_name, model_path, stream_url, conf, iou, width, height):
    """
    Run object detection using YOLOv8 model.

    :param model_name: Name of the YOLOv8 model file.
    :param model_path: Directory path where the model file is stored.
    :param stream_url: URL or path for the video stream or file.
    :param conf: Confidence threshold for detections.
    :param iou: Intersection Over Union threshold for determining unique detections.
    :param width: Camera pixel width.
    :param height: Camera pixel height.
    """
    camera_process = subprocess.Popen([
        'libcamera-vid',
        '-n',
        '-t', '0',
        '--width', str(width),
        '--height', str(height),
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
        results = model.track(source=stream_url, stream=True, conf=conf, iou=iou, tracker="bytetrack.yaml", show=True)
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
    parser = argparse.ArgumentParser(description="Run object detection using a YOLOv8 model on a video stream.")
    parser.add_argument("--model_name", type=str, default="yolov8n.pt", help="Name of the YOLOv8 model file. Default: 'yolov8n.pt'.")
    parser.add_argument("--model_path", type=str, default="models", help="Directory path where the model file is stored. Default: 'models'.")
    parser.add_argument("--stream_url", type=str, default="tcp://127.0.0.1:8888", help="URL or path for the video stream or file. Default: 'tcp://127.0.0.1:8888'.")
    parser.add_argument("--conf", type=float, default=0.5, help="Confidence threshold for detections. Default: 0.5.")
    parser.add_argument("--iou", type=float, default=0.7, help="Intersection Over Union threshold for determining unique detections. Default: 0.7.")
    parser.add_argument("--width", type=int, default=800, help="Camera pixel width. Default: 800.")
    parser.add_argument("--height", type=int, default=640, help="Camera pixel height. Default: 640.")
    
    args = parser.parse_args()

    run_detection(args.model_name, args.model_path, args.stream_url, args.conf, args.iou, args.width, args.height)
