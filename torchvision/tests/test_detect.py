from src.coco_names import COCO_INSTANCE_CATEGORY_NAMES as coco_names
from src.model import get_model
from src.detect_utils import draw_boxes, predict, COLORS
import unittest
from unittest.mock import patch
import torch
import os
import cv2

TEST_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'test_images')

class TestModel(unittest.TestCase):
    def test_get_model(self):
        with patch('src.model.ssdlite320_mobilenet_v3_large'):
            device = torch.device('cpu')
            model = get_model(device)
            self.assertTrue(hasattr(model, 'eval'))

class TestDetectUtils(unittest.TestCase):
    def setUp(self):
        self.device = torch.device('cpu')
        self.model = get_model(self.device)
        self.model.eval()  # Set the model to evaluation mode
        self.image_path = os.path.join(TEST_IMAGES_DIR, 'dog_bike_car.jpg')
        self.image = cv2.imread(self.image_path)
        self.detection_threshold = 0.5

    def test_draw_boxes(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        boxes, classes, labels, scores = predict(rgb_image, self.model, self.device, self.detection_threshold)
        drawn_image = draw_boxes(boxes, classes, labels, scores, rgb_image)
        drawn_image_bgr = cv2.cvtColor(drawn_image, cv2.COLOR_RGB2BGR)
        self.assertGreater(len(boxes), 0, "No boxes drawn on the image")
        cv2.imwrite(os.path.join(TEST_IMAGES_DIR, 'output.jpg'), drawn_image_bgr)

if __name__ == '__main__':
    unittest.main()
