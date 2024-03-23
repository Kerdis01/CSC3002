#!/bin/bash

# install_python_deps.sh

pip install pip --upgrade
pip install argparse
pip install "numpy>=1.20.0"
pip install opencv-python-headless
pip install "tflite==2.3.0"
pip install "tflite_support>=0.4.2"
pip install "protobuf>=3.18.0,<4"

echo "Python dependencies installed."

