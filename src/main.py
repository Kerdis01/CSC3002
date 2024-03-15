# main.py
import cv2
import objectDetector
import faceDetector
import imagePreprocessor
import boundingBoxDrawer

# Initialize detectors
object_model_path = 'mobilenet_object_detection.tflite'
face_model_path = 'mobilenet_facial_recognition.tflite'
object_detector = objectDetector(object_model_path)
face_detector = faceDetector(face_model_path)

# Initialize the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocess the frame for object and face detection
    input_shape_obj = object_detector.input_details[0]['shape']
    input_shape_face = face_detector.input_details[0]['shape']
    preprocessed_frame_obj = imagePreprocessor.preprocess(frame, input_shape_obj)
    preprocessed_frame_face = imagePreprocessor.preprocess(frame, input_shape_face)
    
    # Detect objects and faces
    boxes, classes, scores = object_detector.detect(preprocessed_frame_obj)
    faces = face_detector.detect(preprocessed_frame_face)
    
    # Draw bounding boxes for detected objects and faces
    boundingBoxDrawer.draw_boxes(frame, zip(boxes, scores), (10, 255, 0), label_prefix='Obj ')
    boundingBoxDrawer.draw_boxes(frame, zip(faces), (255, 0, 10), label_prefix='Face ')
    
    # Display the resulting frame
    cv2.imshow('Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
