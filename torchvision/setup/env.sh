#!/bin/bash

# env.sh

echo "Creating and activating the conda environment..."
source $HOME/miniconda3/etc/profile.d/conda.sh
conda create -n tflite_env python=3.8 -y
conda activate tflite_env
exec bash