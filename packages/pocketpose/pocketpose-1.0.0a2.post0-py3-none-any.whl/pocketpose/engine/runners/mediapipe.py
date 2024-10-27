from typing import Any, Dict, List, Tuple, Union

import mediapipe as mp
import numpy as np

from pocketpose.registry import RUNNERS

from .base import BaseRunner


@RUNNERS.register_module()
class MediaPipeRunner(BaseRunner):
    """Runner for MediaPipe models."""

    def __init__(self, model_path: str):
        super().__init__(model_path)

    def build_model(self, model_path: str) -> Any:
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE,
        )

        return PoseLandmarker.create_from_options(options)

    def get_inputs(self) -> List[Dict]:
        return [
            {
                "name": "image",
                "shape": (1, 192, 192, 3),  # FIXME: Shape should be read from the model
                "dtype": np.float16,
            }
        ]

    def get_outputs(self) -> List[Dict]:
        return [{"name": "pose_landmarks", "shape": (33, 5), "dtype": np.float16}]

    def forward(self, image: np.ndarray) -> Any:
        predictions = self.model.detect(image)
        return predictions.pose_landmarks

    def __call__(self, image: np.ndarray) -> Union[np.ndarray, Tuple[np.ndarray]]:
        return self.forward(image)
