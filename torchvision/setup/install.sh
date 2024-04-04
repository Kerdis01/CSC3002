#!/bin/bash

####-RUN 'MAKE' TO INSTALL DEPENDENCIES-####

# Step 1: Install Miniconda
# Ensure the Miniconda3 directory does not already exist to prevent overwriting
if [ ! -d "$HOME/miniconda3" ]; then
    # Download the latest Miniconda3 install script
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $HOME/miniconda3.sh
    
    # Run the installer
    bash $HOME/miniconda3.sh -b -p $HOME/miniconda3

    # Remove the installer script
    rm $HOME/miniconda3.sh
else
    echo "Miniconda3 is already installed at $HOME/miniconda3"
fi

# Initialize Conda
source $HOME/miniconda3/etc/profile.d/conda.sh
conda init

# Re-executing bash to refresh environment and apply conda initialization
exec bash

# Step 2: Create and activate a conda environment
conda create -n tflite_env python=3.8 -y
# Activate the environment
eval "$(conda shell.bash hook)"
conda activate tflite_env

# Step 3: Install Python dependencies
sudo apt-get update
pip install -e 
pip install pip --upgrade
pip install argparse
pip install numpy>=1.20.0
pip install opencv-python-headless
pip install tflite-support>=0.4.2
pip install protobuf>=3.18.0,<4

echo "Installation completed. Environment 'tflite_env' is ready."
exec bash

# Step 4: Install tflite files under /home/kerdis01/CSC3002/src/models

# Define the target directory for the models
DATA_DIR="$HOME/CSC3002/src/models"

# Create the directory if it does not exist
mkdir -p ${DATA_DIR}

# Download TF Lite model with metadata to the specified directory
FILE=${DATA_DIR}/efficientnet_lite0.tflite
if [ ! -f "$FILE" ]; then
  curl \
    -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/image_classification/rpi/lite-model_efficientnet_lite0_uint8_2.tflite' \
    -o ${FILE}
fi

# Download the Edge TPU version of the model to the specified directory
FILE=${DATA_DIR}/efficientnet_lite0_edgetpu.tflite
if [ ! -f "$FILE" ]; then
  curl \
    -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/image_classification/rpi/efficientnet_lite0_edgetpu.tflite' \
    -o ${FILE}
fi

echo -e "Downloaded TensorFlow Lite files are in ${DATA_DIR}"
