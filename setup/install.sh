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

# Step 2: Create and activate a conda environment
conda create -n tflite_env python=3.8 -y
# Activate the environment
eval "$(conda shell.bash hook)"
conda activate tflite_env

# Step 3: Install Python dependencies
sudo apt-get update
pip install -e .
pip install tensorflow==2.3.0
pip install tflite==2.2.0
pip install opencv-python
pip install opencv-python-headless

# Step 4: Verify everything is installed correctly
# (Add any commands for verification if necessary)

echo "Installation completed. Environment 'tflite_env' is ready."
