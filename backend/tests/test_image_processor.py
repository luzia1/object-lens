import numpy as np
from app.services.image_processor import convert_hue_to_coordinates, prepare_color_features, calculate_color_percentages, cluster_colors, extract_object_hsv_pixels

def test_convert_hue_to_coordinates():
    hsv_pixels = np.array([[0, 255, 255]])
    x,y = convert_hue_to_coordinates(hsv_pixels)

    assert np.isclose(x[0], 1)
    assert np.isclose(y[0], 0)

def test_prepare_color_features():
    hsv_pixels = np.array([[0, 255, 255]])
    
    features = prepare_color_features(hsv_pixels)

    assert features.shape == (1, 4)
    assert np.isclose(features[0, 0], 1)
    assert np.isclose(features[0, 1], 0)
    assert np.isclose(features[0, 2], 1)
    assert np.isclose(features[0, 3], 1)

def test_calculate_color_percentages():
    labels = np.array([0, 0, 1, 2, 1, 0, 2, 2])

    percentages = calculate_color_percentages(labels)

    assert np.allclose(percentages, [37.5, 25, 37.5])

def test_cluster_color():
    features = np.array([
        [1, 0, 1, 1],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [-1, 0, 1, 1],
        [-1, 0, 1, 1]
    ])

    results = cluster_colors(features)

    assert len(results) == 3

    percentages = [item["percentage"] for item in results]
    assert np.allclose(percentages, [33.33, 33.33, 33.33], atol=0.01)

def test_cluster_colors_with_one_unique_color():
    features = np.array([
        [1, 0, 1, 1],
        [1, 0, 1, 1],
        [1, 0, 1, 1]
    ])

    results = cluster_colors(features)

    assert len(results) == 1
    assert results[0]["percentage"] == 100.0

def test_extract_object_hsv_pixels_with_empty_mask():
    hsv_image = np.zeros((100, 100, 3), dtype=np.uint8)
    mask = np.zeros((100, 100), dtype=np.uint8)

    pixels = extract_object_hsv_pixels(hsv_image, mask)

    assert pixels.size == 0
    assert pixels.shape == (0, 3)