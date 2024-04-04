#!/bin/bash

# download_tflite_files.sh

DATA_DIR="$HOME/CSC3002/src/models"
mkdir -p ${DATA_DIR}

FILE=${DATA_DIR}/efficientnet_lite0.tflite
if [ ! -f "$FILE" ]; then
    curl -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/image_classification/rpi/lite-model_efficientnet_lite0_uint8_2.tflite' -o ${FILE}
fi

echo "TensorFlow Lite files downloaded to ${DATA_DIR}"
