import numpy as np

from .base_decoder import Decoder


class HeatmapDeocder(Decoder):
    def decode(self, prediction, image_shape):
        assert isinstance(prediction, np.ndarray) and len(prediction.shape) == 3
        assert len(image_shape) == 2

        num_keypoints, heatmap_height, heatmap_width = prediction.shape
        image_height, image_width = image_shape

        # Scale factors for converting heatmap coordinates to image coordinates
        x_scale = image_width / heatmap_width
        y_scale = image_height / heatmap_height

        keypoints = []
        for i in range(num_keypoints):
            # Find the index of the maximum value in the heatmap
            y, x = np.unravel_index(
                np.argmax(prediction[i]), (heatmap_height, heatmap_width)
            )
            score = prediction[i, y, x]

            # Scale the coordinates from heatmap space to image space
            x = x * x_scale
            y = y * y_scale

            keypoints.append((int(x), int(y), score))

        return keypoints
