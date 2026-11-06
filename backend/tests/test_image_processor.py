import numpy as np
from app.services.image_processor import convert_hue_to_coordinates, prepare_color_features, calculate_color_percentages

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