# CSC3002 - Raspberry Pi Object Detector Project

Install Requirements for "Final" System

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
  
