from typing import List

import numpy as np
from tensorflow.keras.applications.imagenet_utils import (
    preprocess_input as efficientnet_preprocess_input,
)

from pocketpose.models.decoder import HeatmapDeocder
from pocketpose.registry import DATASETS, POSE_ESTIMATORS

from .base import IModel


def normalize_image(image: np.ndarray, mean: tuple, std: tuple) -> np.ndarray:
    """Normalize the image using the given mean and standard deviation values."""
    image = image.astype("float32")
    image[..., :] -= mean
    image[..., :] /= std
    return image


class TopdownHeatmapModel(IModel):
    """Base class for LiteHRNet models."""

    def __init__(self, model_variant: str, **kwargs):
        super().__init__("topdown_heatmap.json", model_variant, **kwargs)
        self.decoder = HeatmapDeocder()

    def process_image(self, image: np.ndarray) -> np.ndarray:
        return normalize_image(
            image, mean=(123.675, 116.28, 103.53), std=(58.395, 57.12, 57.375)
        ).transpose(0, 3, 1, 2)

    def postprocess_prediction(self, prediction, original_size) -> List[List[float]]:
        return self.decoder.decode(prediction.squeeze(), tuple(original_size))


@POSE_ESTIMATORS.register_module()
class LiteHRNet18(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("litehrnet-18_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class LiteHRNet30(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("litehrnet-30_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class MobileNetV2(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("mobilenetv2_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class ShuffleNetV1(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("shufflenetv1_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class ShuffleNetV2(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("shufflenetv2_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class AlexNet(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("alexnet_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class LPN50(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("lpn-50_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class LPN101(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("lpn-101_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class LPN152(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("lpn-152_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class LPN50M(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("lpn-50_mpii", **kwargs)


@POSE_ESTIMATORS.register_module()
class NASNetA(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("nasnet-a_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class NASNetB(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("nasnet-b_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class NASNetC(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("nasnet-c_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class NASNetB16(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("nasnet-b_mpii", **kwargs)


@POSE_ESTIMATORS.register_module()
class NASNetC16(TopdownHeatmapModel):
    def __init__(self, **kwargs):
        super().__init__("nasnet-c_mpii", **kwargs)


class EfficientPose(TopdownHeatmapModel):
    """Base class for EfficientPose models."""

    def __init__(self, model_variant: str, lite: bool = False, **kwargs):
        super().__init__(model_variant, **kwargs)
        self.lite = lite

        # Precompute the mapping for reordering the keypoints
        expected_order = list(DATASETS.build("mpii").nodes.values())
        current_order = [
            "head_top",
            "upper_neck",
            "right_shoulder",
            "right_elbow",
            "right_wrist",
            "thorax",
            "left_shoulder",
            "left_elbow",
            "left_wrist",
            "pelvis",
            "right_hip",
            "right_knee",
            "right_ankle",
            "left_hip",
            "left_knee",
            "left_ankle",
        ]
        self.mapping = np.array([current_order.index(part) for part in expected_order])

    def process_image(self, image):
        if not self.lite:
            image = efficientnet_preprocess_input(image, mode="torch")

        return image

    def postprocess_prediction(self, prediction, original_size):
        if not self.lite:
            prediction = prediction[-1]  # Use only the last prediction

        prediction = prediction.transpose(0, 3, 1, 2)  # NhwC -> NChw
        prediction = prediction[:, self.mapping]
        return super().postprocess_prediction(prediction, original_size)


@POSE_ESTIMATORS.register_module()
class EfficientPoseRTLite(EfficientPose):
    def __init__(self, **kwargs):
        super().__init__("efficientpose-rt-lite_mpii", lite=True, **kwargs)


@POSE_ESTIMATORS.register_module()
class EfficientPoseILite(EfficientPose):
    def __init__(self, **kwargs):
        super().__init__("efficientpose-i-lite_mpii", lite=True, **kwargs)


@POSE_ESTIMATORS.register_module()
class EfficientPoseIILite(EfficientPose):
    def __init__(self, **kwargs):
        super().__init__("efficientpose-ii-lite_mpii", lite=True, **kwargs)


@POSE_ESTIMATORS.register_module()
class EfficientPoseRT(EfficientPose):
    def __init__(self, **kwargs):
        super().__init__("efficientpose-rt_mpii", **kwargs)


@POSE_ESTIMATORS.register_module()
class EfficientPoseI(EfficientPose):
    def __init__(self, **kwargs):
        super().__init__("efficientpose-i_mpii", **kwargs)


@POSE_ESTIMATORS.register_module()
class EfficientPoseII(EfficientPose):
    def __init__(self, **kwargs):
        super().__init__("efficientpose-ii_mpii", **kwargs)


@POSE_ESTIMATORS.register_module()
class EfficientPoseIII(EfficientPose):
    def __init__(self, **kwargs):
        super().__init__("efficientpose-iii_mpii", **kwargs)


@POSE_ESTIMATORS.register_module()
class EfficientPoseIV(EfficientPose):
    def __init__(self, **kwargs):
        super().__init__("efficientpose-iv_mpii", **kwargs)
