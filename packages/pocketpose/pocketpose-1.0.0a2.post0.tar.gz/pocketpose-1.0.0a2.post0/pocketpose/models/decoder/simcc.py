import numpy as np

from .base_decoder import Decoder


class SimCCDecoder(Decoder):
    def decode(self, prediction, image_shape):
        assert isinstance(prediction, tuple) and len(prediction) == 2
        assert isinstance(image_shape, tuple) and len(image_shape) == 2

        simcc_x, simcc_y = prediction
        image_height, image_width = image_shape

        # Compute scaling factors
        k_x = simcc_x.shape[-1] / image_width
        k_y = simcc_y.shape[-1] / image_height

        # Compute horizontal and vertical keypoint coordinates in image space
        kpts_x = (np.argmax(simcc_x, axis=2) / k_x).flatten()
        kpts_y = (np.argmax(simcc_y, axis=2) / k_y).flatten()

        # Compute keypoint scores as the average of the horizontal and vertical scores
        kpts_score = (np.max(simcc_x, axis=2) + np.max(simcc_y, axis=2)) / 2
        kpts_score = kpts_score.flatten()

        # Convert coordinates to int but keep score as float
        return [[int(x), int(y), s] for x, y, s in zip(kpts_x, kpts_y, kpts_score)]
