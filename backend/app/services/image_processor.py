import cv2
import numpy as np


def decode_image(contents: bytes):
    image_array = np.frombuffer(contents, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    return image