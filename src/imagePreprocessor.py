# image_preprocessor.py
import cv2
import numpy as np

class ImagePreprocessor:
    @staticmethod
    def preprocess(image, input_shape):
        # Assuming the input_shape includes the required size
        image = cv2.resize(image, (input_shape[1], input_shape[2]))
        input_data = np.expand_dims(image / 255.0, axis=0).astype(np.float32)
        return input_data
