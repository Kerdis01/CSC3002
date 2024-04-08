import unittest
from unittest.mock import patch, MagicMock
import os
from src.detectv3 import run_detection

TEST_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'test_images')

class TestModelInference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_image_path = os.path.join(TEST_IMAGES_DIR, 'dog_bike_car.jpg')
        cls.model_name = 'quantised_yolov8n.pt'
        cls.model_path = 'models'

    @patch('src.detectv3.YOLO')
    def test_inference_on_image(self, mock_yolo):
        mock_model_instance = mock_yolo.return_value
        mock_inference_result = MagicMock()
        mock_inference_result.boxes = [[10, 10, 20, 20]]
        mock_inference_result.speed = {'inference': 100}
        mock_model_instance.track.return_value = [mock_inference_result]

        run_detection(self.model_name, self.model_path, self.test_image_path)

        mock_model_instance.track.assert_called_once_with(
            source=self.test_image_path, 
            stream=True, 
            conf=0.5, 
            iou=0.7, 
            tracker="bytetrack.yaml", 
            show=True
        )

if __name__ == '__main__':
    unittest.main()
