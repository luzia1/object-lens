import numpy as np
from unittest.mock import MagicMock
from app.services.object_segmenter import get_masks

mask_1 = np.array([
    [0, 1],
    [1, 1]
])

mask_2 = np.array([
    [1, 0],
    [0, 1]
])

result = MagicMock()

mask_mock_1 = MagicMock()
mask_mock_2 = MagicMock()

result.masks.data = [mask_mock_1, mask_mock_2]

mask_mock_1.cpu().numpy.return_value = mask_1
mask_mock_2.cpu().numpy.return_value = mask_2

result.boxes.cls = [
    MagicMock(),
    MagicMock()
]

result.boxes.cls[0].item.return_value = 0
result.boxes.cls[1].item.return_value = 39

result.boxes.conf = [
    MagicMock(),
    MagicMock()
]

result.boxes.conf[0].item.return_value = 0.91
result.boxes.conf[1].item.return_value = 0.87

result.names = {
    0: "person",
    39: "bottle"
}

def test_get_masks():
    masks = get_masks(result) 

    assert np.array_equal(masks[0]["mask"], mask_1 * 255)
    assert np.array_equal(masks[1]["mask"], mask_2 * 255)

    assert masks[0]["class_id"] == 0
    assert masks[0]["class_name"] == "person"

    assert masks[1]["class_id"] == 39
    assert masks[1]["class_name"] == "bottle"

    assert masks[0]["confidence"] == 0.91
    assert masks[1]["confidence"] == 0.87

    assert masks[0]["object_id"] == 1
    assert masks[1]["object_id"] == 2

    assert len(masks) == 2