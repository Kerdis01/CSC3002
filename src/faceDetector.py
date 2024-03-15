# face_detection.py
import numpy as np
from tflite_runtime.interpreter import Interpreter

class FaceDetector:
    def __init__(self, model_path):
        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
    
    def detect(self, image):
        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        self.interpreter.invoke()
        # Depending on your model's output, adjust the index below
        faces = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        return faces
