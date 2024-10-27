from typing import Any, Dict, List, Tuple, Union

import numpy as np
import tensorflow as tf

from pocketpose.registry import RUNNERS

from .base import BaseRunner


@RUNNERS.register_module()
class TFLiteRunner(BaseRunner):
    """Runner for TensorFlow Lite models."""

    def __init__(self, model_path: str):
        super().__init__(model_path)

    def build_model(self, model_path: str) -> Any:
        model = tf.lite.Interpreter(model_path=model_path)
        model.allocate_tensors()
        return model

    def get_inputs(self) -> List[Dict]:
        return self.model.get_input_details()

    def get_outputs(self) -> List[Dict]:
        return self.model.get_output_details()

    def forward(self, image: np.ndarray) -> Union[np.ndarray, Tuple[np.ndarray]]:
        # Forward pass
        input_tensor = self.inputs[0]["index"]
        self.model.set_tensor(input_tensor, image)
        self.model.invoke()

        # Read outputs
        outputs = [
            self.model.get_tensor(self.outputs[i]["index"])
            for i in range(self.num_outputs)
        ]

        return tuple(outputs) if self.num_outputs > 1 else outputs[0]
