import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Union

import numpy as np


class BaseRunner(ABC):
    """Base class for model runners.

    Args:
        model_path (str): Path of the model file.
    """

    def __init__(self, model_path: str) -> None:
        # Build the model
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        self.model = self.build_model(model_path)

        # Read model input info
        self.inputs = self.get_inputs()
        if len(self.inputs) != 1:
            raise RuntimeError(
                "Only models with a single input are currently supported."
            )
        if len(self.inputs[0]["shape"]) != 4:
            raise RuntimeError(
                "Only models which accept an image input as a 4D tensor are currently supported."
            )

        self.input_shape = self.inputs[0]["shape"]
        self.input_dtype = self.inputs[0]["dtype"]

        # Read model output info
        self.outputs = self.get_outputs()
        self.num_outputs = len(self.outputs)
        if self.num_outputs == 0:
            raise RuntimeError("Model must have at least one output.")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    @abstractmethod
    def build_model(self, model_path: str) -> Any:
        pass

    @abstractmethod
    def get_inputs(self) -> List[Dict]:
        pass

    @abstractmethod
    def get_outputs(self) -> List[Dict]:
        pass

    @abstractmethod
    def forward(self, image: np.ndarray) -> Union[np.ndarray, Tuple[np.ndarray]]:
        pass

    def __call__(self, image: np.ndarray) -> Union[np.ndarray, Tuple[np.ndarray]]:
        image = image.astype(self.input_dtype)
        return self.forward(image)
