from typing import Any, Dict, List, Tuple, Union

import numpy as np
import onnxruntime as rt

from pocketpose.registry import RUNNERS

from .base import BaseRunner


@RUNNERS.register_module()
class ONNXRunner(BaseRunner):
    """Runner for ONNX models."""

    def __init__(self, model_path: str):
        super().__init__(model_path)

    def build_model(self, model_path: str) -> Any:
        return rt.InferenceSession(model_path)

    def get_inputs(self) -> List[Dict]:
        return [
            {"name": i.name, "shape": i.shape, "dtype": np.float32}  # FIXME: i.type
            for i in self.model.get_inputs()
        ]

    def get_outputs(self) -> List[Dict]:
        return [
            {"name": o.name, "shape": o.shape, "dtype": o.type}
            for o in self.model.get_outputs()
        ]

    def forward(self, image: np.ndarray) -> Union[np.ndarray, Tuple[np.ndarray]]:
        input_tensor = {self.inputs[0]["name"]: image}
        output_tensors = [o["name"] for o in self.outputs]
        outputs = self.model.run(output_tensors, input_tensor)
        return tuple(outputs) if self.num_outputs > 1 else outputs[0]
