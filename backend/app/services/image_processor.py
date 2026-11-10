import cv2
import numpy as np
from sklearn.cluster import KMeans

def decode_image(contents: bytes):
    image_array = np.frombuffer(contents, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    return image

def convert_to_hsv(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    return hsv_image

def extract_object_hsv_pixels(hsv_image, mask):
    object_hsv_pixels = hsv_image[mask == 255]

    return object_hsv_pixels

def convert_hue_to_coordinates(hsv_pixels):
    hue = hsv_pixels[:, 0]

    theta = hue * (2 * np.pi / 180)

    x = np.cos(theta)
    y = np.sin(theta)

    return x, y

def prepare_color_features(hsv_pixels):
    x,y = convert_hue_to_coordinates(hsv_pixels)
    saturation = hsv_pixels[:, 1] / 255.0
    value = hsv_pixels[:, 2] / 255.0

    features = np.column_stack((x, y, saturation, value))

    return features

def cluster_colors(features):
    unique_features = np.unique(features, axis=0)
    n_clusters = min(3, len(unique_features))

    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    kmeans.fit(features)
    
    percentages = calculate_color_percentages(kmeans.labels_)

    colors = []

    for centroid in kmeans.cluster_centers_:
        rgb = convert_centroid_to_rgb(centroid)
        colors.append(rgb)
    
    results = []

    for color, percentage in zip(colors, percentages):
        results.append({
            "color": color,
            "percentage": round(float(percentage), 2)
        })

    results.sort(key=lambda item: item["percentage"], reverse=True)

    return results

def calculate_color_percentages(labels):
    counts = np.bincount(labels)

    percentages = (counts/ len(labels)) * 100

    return percentages

def convert_centroid_to_rgb(centroid):
    x, y, saturation, value = centroid

    theta = np.arctan2(y, x)
    hue = (theta % (2 * np.pi)) * 180 / (2 * np.pi)

    hsv = np.array([[[
        round(hue),
        round(saturation * 255),
        round(value * 255)
    ]]], dtype=np.uint8)

    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    return rgb[0, 0].tolist()