from typing import Any

import mediapipe as mp

from pocketpose.models.decoder import MoveNetDecoder
from pocketpose.registry import POSE_ESTIMATORS

from .base import IModel


class TopdownKeypointModel(IModel):
    """Base class for top-down keypoint models."""

    def __init__(self, model_key: str, **kwargs):
        super().__init__("topdown_keypoint.json", model_key, **kwargs)


class MoveNet(TopdownKeypointModel):
    """Base class for the MoveNet models."""

    def __init__(self, model_key: str, **kwargs):
        super().__init__(model_key, **kwargs)
        self.decoder = MoveNetDecoder()

    def postprocess_prediction(self, prediction, original_size):
        return self.decoder.decode(prediction.squeeze(), original_size)


@POSE_ESTIMATORS.register_module()
class MoveNetLightning(MoveNet):
    def __init__(self, **kwargs):
        super().__init__("movenet-lightning_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class MoveNetThunder(MoveNet):
    def __init__(self, **kwargs):
        super().__init__("movenet-thunder_coco", **kwargs)


class BlazePose(TopdownKeypointModel):
    def __init__(self, model_key: str, **kwargs):
        super().__init__(model_key, **kwargs)

    def process_image(self, image):
        return mp.Image(image_format=mp.ImageFormat.SRGB, data=image[0])

    def postprocess_prediction(
        self, prediction: Any, original_size: tuple
    ) -> list[tuple[float]]:
        if len(prediction) == 0:
            return []

        keypoints = []
        for landmark in prediction[0]:
            x = int(landmark.x * original_size[1])
            y = int(landmark.y * original_size[0])
            score = landmark.presence
            keypoints.append((x, y, score))
        return keypoints


@POSE_ESTIMATORS.register_module()
class BlazePoseLite(BlazePose):
    def __init__(self, **kwargs):
        super().__init__("blazepose-lite", **kwargs)


@POSE_ESTIMATORS.register_module()
class BlazePoseFull(BlazePose):
    def __init__(self, **kwargs):
        super().__init__("blazepose-full", **kwargs)


@POSE_ESTIMATORS.register_module()
class BlazePoseHeavy(BlazePose):
    def __init__(self, **kwargs):
        super().__init__("blazepose-heavy", **kwargs)
