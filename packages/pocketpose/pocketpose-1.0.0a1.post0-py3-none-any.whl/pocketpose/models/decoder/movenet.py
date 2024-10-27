import numpy as np

from .base_decoder import Decoder


class MoveNetDecoder(Decoder):
    def decode(self, prediction, image_shape):
        assert isinstance(prediction, np.ndarray) and len(prediction.shape) == 2
        assert len(image_shape) == 2

        # MoveNet outputs keypoints in the range [0, 1], so we need to rescale them
        # back to the original image size to get the correct coordinates
        keypoints = prediction  # (17, 3) as (y, x, score)
        keypoints[:, :2] *= image_shape

        # Convert coordinates to int but keep score as float
        # Note: MoveNet returns coordinates as (y, x) instead of (x, y)
        #       and we need to convert them to (x, y) to be consistent with
        #       our internal representation.
        keypoints = [tuple([int(x), int(y), s]) for y, x, s in keypoints]

        return keypoints  # (17, 3) as (x, y, score)
