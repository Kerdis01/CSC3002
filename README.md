# CSC3002 - Raspberry Pi Object Detector Project

This project guides you through setting up three different Machine Learning models for object detection on a Raspberry Pi. Each model requires a specific setup as outlined below.

## Table of Contents
- [1. TensorFlow Lite (WIP)](#1-tensorflow-lite-wip)
- [2. YOLOv5 Setup](#2-yolov5-setup)
- [3. YOLOv8 Setup](#3-yolov8-setup)

---

## 1. TensorFlow Lite (WIP)
*This section is a work in progress and will be updated soon.*

---

## 2. YOLOv5 Setup

Follow these steps to set up and run the YOLOv5 object detection model:

### Step 1: Activate Environment
Navigate to the YOLOv5 directory and activate the virtual environment:

cd yolov5
python -m venv yolov5_env
source yolov5_env/bin/activate


### Step 2: Build YOLOv5
Compile the YOLOv5 environment using `make`:

make

### Step 3: Run the Object Detection
Execute the libcamera command and start the object detection script:

libcamera-vid -n -t 0 --width 1280 --height 960 --framerate 1 --inline --listen -o tcp://127.0.0.1:8888
python detect.py

---

## 3. YOLOv8 Setup

To use YOLOv8 for object detection, follow the instructions below:

### Step 1: Activate Environment
Change to the YOLOv8 directory and set up the virtual environment:

cd yolov8
python -m venv yolov8_env
source yolov8_env/bin/activate

### Step 2: Build YOLOv8
Prepare the YOLOv8 environment:

make

### Step 3: Start Object Detection
Run the libcamera command and initiate the detection script:

libcamera-vid -n -t 0 --width 1280 --height 960 --framerate 1 --inline --listen -o tcp://127.0.0.1:8888
python detect.py
