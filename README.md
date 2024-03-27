# CSC3002
Raspberry Pi Object Detector Project

For tflite, run:

################

For yolov5, run:

cd yolov5

python -m venv yolov5_env

source yolov5_env/bin/activate

make

libcamera-vid -n -t 0 --width 1280 --height 960 --framerate 1 --inline --listen -o tcp://127.0.0.1:8888

python detect.py

###############

For yolov8, run:

cd yolov8

python -m venv yolov8_env

source yolov8_env/bin/activate

make

libcamera-vid -n -t 0 --width 1280 --height 960 --framerate 1 --inline --listen -o tcp://127.0.0.1:8888

python detect.py

