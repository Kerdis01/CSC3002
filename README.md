# CSC3002 - Raspberry Pi Object Detector Project

Install Requirements for **"Final"** System

1. Clone the repository to your desired destination.

2. Create a virtual environment within the final system's directory:

  ```cd final```

  ```python3 -m venv .venv```

  ```source .venv/bin/activate```

3. Install the python libraries (this will take some time):

  ```python3 -m pip install -r setup/requirements.txt```

4. Run the script, which will use a YOLOv8 model and run real time object detection using your camera stream:

   ```python3 src/detect_video.py```

5. Use the --help flag to see the full list of parameters that can be specified:

  ```python3 src/detect_video.py --help```

6. To stop running the script, use CTRL+C for a Keyboard Interruption

#########################################################################################

**Running the Experimental Systems:**
  
Install Requirements for **"torchvision"** System

1. Clone the repository to your desired destination.

2. Create a virtual environment within the torchvision system's directory:

  ```cd torchvision```

  ```python3 -m venv .venv```

  ```source .venv/bin/activate```

3. Install the python libraries (this will take some time):

  ```make```

4. Comment out the "upload_to_s3" line at the end of the script.

5. Run the script, which will use a SSDLITE_MOBILE_NET_V3_LARGE model and run real time object detection using your camera stream:

   ```python3 src/detect_video.py```

#########################################################################################

Install Requirements for **"yolov8"** System

1. Clone the repository to your desired destination.

2. Create a virtual environment within the torchvision system's directory:

  ```cd yolov8```

  ```python3 -m venv .venv```

  ```source .venv/bin/activate```

3. Install the python libraries (this will take some time):

  ```make```

4. Comment out the "upload_to_s3" line at the end of the script.

5. Run the script, which will use a YOLOv8 Nano model and run real time object detection using your camera stream:

   ```python3 src/detect_video.py```

#########################################################################################
  
**Both of these experimental systems shall create CSV files after 100 frames of inference showing the metrics of these systems during runtime. **
