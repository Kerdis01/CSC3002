# bounding_box_drawer.py
import cv2

class BoundingBoxDrawer:
    @staticmethod
    def draw_boxes(image, items, color, label_prefix=''):
        for item in items:
            y_min, x_min, y_max, x_max, score = item
            if score > 0.5:  # Threshold can be adjusted
                x_min = int(x_min * image.shape[1])
                x_max = int(x_max * image.shape[1])
                y_min = int(y_min * image.shape[0])
                y_max = int(y_max * image.shape[0])
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
                label = f"{label_prefix}{score:.2f}"
                cv2.putText(image, label, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
