import cv2
import numpy as np
import tensorflow as tf

class CameraObjectDetector:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        _, self.input_height, self.input_width, _ = self.input_details[0]['shape']

    def preprocess(self, frame):
        frame_resized = cv2.resize(frame, (self.input_width, self.input_height))
        input_data = np.expand_dims(frame_resized, axis=0).astype(np.float32)
        input_mean, input_std = 127.5, 127.5
        input_data = (input_data - input_mean) / input_std
        return input_data

    def postprocess(self, frame, boxes, classes, scores, count):
        for i in range(count):
            if scores[i] > 0.5:  # Only consider detections with a confidence > 50%
                ymin, xmin, ymax, xmax = boxes[i]
                xmin = int(xmin * self.input_width)
                xmax = int(xmax * self.input_width)
                ymin = int(ymin * self.input_height)
                ymax = int(ymax * self.input_height)

                # Draw the bounding box and label on the frame
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                label = f"{classes[i]}: {int(scores[i]*100)}%"
                cv2.putText(frame, label, (xmin, ymax), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        return frame

    def detect_objects(self, image):
        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        self.interpreter.invoke()
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
        count = self.interpreter.get_tensor(self.output_details[3]['index'])[0]
        return boxes, classes, scores, count

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        print("Camera opened successfully.")
        frame_count = 0  # Counter for the number of frames processed
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
        
            # Process frame for object detection.
            input_data = self.preprocess(frame)
            boxes, classes, scores, count = self.detect_objects(input_data)
            frame = self.postprocess(frame, boxes, classes, scores, count)

            # Increment and print the frame count every 100 frames.
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Processed {frame_count} frames")

            # Display the resulting frame with bounding boxes
            cv2.imshow('Object Detection', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) == ord('q'):
                print("Quitting the application...")
            break

        cap.release()
        cv2.destroyAllWindows()
        print("Camera feed has been released and windows are closed.")

# Example usage:
detector = CameraObjectDetector('models/efficientNetLite2.tflite')
detector.run()