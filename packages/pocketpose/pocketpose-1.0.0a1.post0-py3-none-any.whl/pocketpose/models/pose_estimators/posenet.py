import os
from typing import List

import numpy as np

from pocketpose.core.config import load_cfg
from pocketpose.models.decoder import PoseNetDecoder
from pocketpose.models.interfaces import TFLiteModel
from pocketpose.registry import POSE_ESTIMATORS


class PoseNet(TFLiteModel):
    """Base class for PoseNet models."""

    def __init__(self, model_variant: str, output_stride=16):
        """Initialize the model.

        Args:
            model_variant (str): The model variant to use. Can only be 'mb100' for now.
            output_stride (int): The output stride of the model. Can be 8, 16, or 32.
        """
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cfg_file = os.path.join(root_dir, "../configs/posenet.json")
        cfg = load_cfg(cfg_file, model_variant)
        self.name = cfg["name"]
        self.description = cfg["description"]
        self.paper = cfg["paper"]
        self.type = cfg["type"]
        self.decoder = PoseNetDecoder(output_stride=output_stride)
        super().__init__(
            cfg["cache_path"],
            cfg["url"],
            keypoints_type=cfg["keypoints"],
            input_size=cfg["input_size"],
        )

    def process_image(self, image):
        # PoseNet expects the image to be in the range [-1, 1]
        image = (image / 255) * 2 - 1
        return image

    def postprocess_prediction(self, prediction, original_size) -> List[List[float]]:
        heatmaps, offsets, displacement_fwd, displacement_bwd = prediction

        # Remove batch dimension
        heatmaps = heatmaps.squeeze()  # (9, 9, 17)
        offsets = offsets.squeeze()  # (9, 9, 34)
        displacement_fwd = displacement_fwd.squeeze()  # (9, 9, 32)
        displacement_bwd = displacement_bwd.squeeze()  # (9, 9, 32)
        print(
            heatmaps.shape,
            offsets.shape,
            displacement_fwd.shape,
            displacement_bwd.shape,
        )

        scaled_size = tuple(np.array(original_size) / self.input_size[:2])
        keypoints = self.decoder.decode((heatmaps, offsets), scaled_size)

        return keypoints


@POSE_ESTIMATORS.register_module()
class PoseNetSinglePerson(PoseNet):
    def __init__(self):
        super().__init__("mb100", output_stride=32)
