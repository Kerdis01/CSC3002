# CSC3002 - Raspberry Pi Object Detector Project

Install Requirements for "Final" System

1. Clone the repository to your desired destination

2. Create a virtual environment within the final system's directory

  ```cd final```

  ```python3 -m venv .venv```

  ```source .venv/bin/activate```

3. Install the python libraries (this will take some time)

  ```python3 -m pip install -r setup/requirements.txt```

4. Run the camera script

   ```python3 src/detect_video.py```

   
This will install the Ultralytics library and run inference using a quantised YOLOv8 model.
