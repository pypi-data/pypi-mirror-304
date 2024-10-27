import numpy as np

from .base_decoder import Decoder


class PoseNetDecoder(Decoder):

    def __init__(self, output_stride=32):
        self.output_stride = (
            output_stride * 4
        )  # NOTE: x4 is a hack, the decoder needs to be fixed

    def _decode_unrefined(self, prediction):
        assert isinstance(prediction, np.ndarray) and len(prediction.shape) == 3
        num_keypoints, heatmap_height, heatmap_width = prediction.shape
        keypoints = []
        for i in range(num_keypoints):
            y, x = np.unravel_index(
                np.argmax(prediction[i]), (heatmap_height, heatmap_width)
            )
            score = prediction[i, y, x]
            keypoints.append((x, y, score))
        return keypoints

    def _refine(self, keypoints, offsets):
        refined_keypoints = []
        for i, (x, y, score) in enumerate(keypoints):
            x_offset, y_offset = offsets[x, y, 2 * i : 2 * i + 2]
            refined_x = x * self.output_stride + x_offset
            refined_y = y * self.output_stride + y_offset
            refined_keypoints.append((refined_x, refined_y, score))
        return np.array(refined_keypoints)

    def decode(self, prediction, image_shape):
        assert (
            isinstance(prediction, tuple) and len(prediction) == 2
        ), "PoseNetDecoder expects a tuple of (heatmaps, offsets) as input."

        heatmaps, offsets = prediction
        heatmaps = heatmaps.transpose(2, 0, 1)

        assert isinstance(heatmaps, np.ndarray) and len(heatmaps.shape) == 3
        assert isinstance(offsets, np.ndarray) and len(offsets.shape) == 3
        assert isinstance(image_shape, tuple) and len(image_shape) == 2

        keypoints = self._decode_unrefined(heatmaps)
        keypoints = self._refine(keypoints, offsets)
        keypoints[:, 0] = keypoints[:, 0] / image_shape[0]
        keypoints[:, 1] = keypoints[:, 1] / image_shape[1]
        return [[int(x), int(y), s] for x, y, s in keypoints]
