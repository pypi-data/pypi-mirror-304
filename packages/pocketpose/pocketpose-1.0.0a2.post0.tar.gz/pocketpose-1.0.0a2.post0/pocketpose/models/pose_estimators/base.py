""" Defines the interface for PocketPose models. """

import logging
import os
import time
import warnings
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

from pocketpose.core.config import load_cfg
from pocketpose.registry import RUNNERS
from pocketpose.utils import download_file

logger = logging.getLogger(__name__)


class IModel(ABC):
    """Base class for all models.

    This class defines the interface that all models must implement. The interface
    is designed to be as generic as possible, so that it can be used with any model.

    The model class hierarchy is as follows:
    IModel
    ├── Framework-specific interface (e.g. TFLiteModel)
    │   ├── Model class (e.g. MoveNet)

    The interface is divided into four steps:
    1. Load the input image
    2. Prepare the image for prediction
    3. Run inference
    4. Postprocess the prediction to get the keypoints

    The first step is model-agnostic, so it is implemented in this class. Step 3 is
    specific to the framework, so it is implemented in the framework-specific interface
    which is a subclass of this class. Steps 2 and 4 are model-specific, so they are
    implemented in the model classes which are subclasses of the framework-specific
    interfaces.
    """

    def __init__(
        self,
        config_file: str,
        model_key: str,
        info_mode: bool = False,
    ):
        """Initialize the model.

        Args:
            config_file (str): The path to the model configuration file.
            model_key (str): The key of the model configuration to use.
            info_mode (bool): Set true to create the model in info mode, which
                              disables downloading and inference. This is useful
                              for getting information about the model without
                              actually running it.
        """
        # Read the model configuration
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cfg_file = os.path.join(root_dir, "..", "configs", config_file)
        cfg = load_cfg(cfg_file, model_key)
        self.cfg = cfg

        # Set the model attributes
        self.model_path = cfg.cache_path
        self.model_url = cfg.download_path
        self.keypoints_type = cfg.skeleton
        self.input_size = cfg.input_size
        self.input_height = cfg.input_size[0]
        self.input_width = cfg.input_size[1]
        self.input_channels = cfg.input_size[2]
        self.last_inference_duration_ms = 0

        # Download the model file if it does not exist
        if info_mode:
            self.runner = None
            return

        if not os.path.exists(self.model_path):
            warnings.warn("Model file does not exist. It will be downloaded now.")
            success = download_file(self.model_url, self.model_path)
            if not success:
                raise FileNotFoundError(
                    f"Could not download model file from {self.model_url}."
                )

        # Create the model runner
        runner = cfg.runner
        try:
            self.runner = RUNNERS.build(runner, model_path=self.model_path)
            logger.info(f"Using runner: {self.runner}")
        except ValueError:
            raise ValueError(f'Requested runner "{runner}" is not available')
        except Exception:
            raise RuntimeError(f'Could not create runner for model "{self.model_path}"')

    def get_info(self) -> Dict:
        """Returns information about the model."""
        return self.cfg.as_dict()

    def load_image(
        self, image_path: str, crop_bbox=None
    ) -> tuple[np.ndarray, tuple[int]]:
        """Loads an image from a file.

        The image is loaded using the TensorFlow I/O library, and is resized to
        match the model input size using bilinear interpolation. The aspect ratio
        is preserved by padding the shorter side with zeros.

        Args:
            image_path (str): Path to the image file.

        Returns:
            The loaded image as a numpy array with shape (1, height, width, channels)
            and dtype uint8 (range [0, 255]).
            The original size of the image as a tuple (height, width).
        """
        if isinstance(image_path, str):
            # Load the input image as a 3-channel numpy array using PIL
            image = Image.open(image_path).convert("RGB")
            image = np.array(image)
            original_size = image.shape[:2]
        elif isinstance(image_path, np.ndarray):
            image = image_path
            original_size = image.shape[:2]
        else:
            raise ValueError(
                "Invalid image type. Expected str or numpy array, got: ",
                type(image_path),
            )

        # Crop the image (if bounding box provided)
        if crop_bbox is not None:
            x1, y1, x2, y2 = crop_bbox
            image = image[y1:y2, x1:x2]
            original_size = (y2 - y1, x2 - x1)

        # Resize and pad the image to keep the aspect ratio and fit the expected size.
        input_image = np.array(
            Image.fromarray(image).resize((self.input_width, self.input_height))
        )
        input_image = np.expand_dims(
            input_image, axis=0
        )  # Add batch dimension again after resizing

        # Convert the image to a numpy array and cast to uint8
        input_image = input_image.astype(np.uint8)

        return input_image, original_size  # type: ignore

    def process_image(self, image: np.ndarray) -> np.ndarray:
        """Prepares the image for prediction.

        Args:
            image (np.ndarray): The image to prepare for prediction. The image
                                has shape (1, height, width, channels) and dtype
                                uint8 (range [0, 255]).

        Returns:
            The processed image as a numpy array with the shape and dtype expected
            by the model.
        """
        return image

    def predict(self, image: np.ndarray) -> Any:
        """Predicts the pose of the image.

        Args:
            image (np.ndarray): The image to predict the pose of. The image has
                                the shape and dtype expected by the model.

        Returns:
            The prediction returned by the model. This can be a single tensor or
            a tuple of tensors, depending on the model.
        """
        return self.runner(image)

    @abstractmethod
    def postprocess_prediction(
        self, prediction: Any, original_size: tuple
    ) -> List[tuple[float]]:
        """Postprocesses the prediction to get the keypoints.

        Args:
            prediction (Any): The raw prediction returned by the model. This can
                              be a single tensor or a tuple of tensors, depending
                              on the model.
            original_size (tuple): The original size of the input image as (height, width).

        Returns:
            The predicted keypoints as a list of (x, y, score) tuples.
        """
        raise NotImplementedError()

    def __call__(
        self, image_path: str, crop_bbox: Optional[Tuple] = None
    ) -> List[tuple[float]]:
        """Infers the pose of an image.

        Args:
            image_path (str): Path to the image file.

        Returns:
            The predicted keypoints as a list of (x, y, score) tuples.
        """
        # Step 1: Load the input image
        # In this step, the image is loaded from a file and resized to match
        # the model input size. However, the image is not normalized or otherwise
        # preprocessed, as this is model-specific.
        image, original_size = self.load_image(image_path, crop_bbox)

        # Step 2: Prepare the image for prediction (model-specific)
        # This step receives the image as a numpy array of shape (1, height, width, 3)
        # and dtype uint8 (range [0, 255]), and performs model-specific preprocessing
        # such as normalization, data type conversion, etc. The output of this step
        # should be whatever the model expects as input.
        image = self.process_image(image)  # Model-specific normalization, etc.

        # Step 3: Run inference
        # In this step, the model is run on the input image and the output is returned.
        # The output is not necessarily the final prediction, because some models predict
        # heatmaps, while others even have multiple outputs. This is why we need the
        # next step, which receives the raw model output and converts it to a list of
        # tuples where each tuple contains the (x, y, score) values of a keypoint.
        time_start = time.time()
        prediction = self.predict(image)
        time_end = time.time()
        self.last_inference_duration_ms = (time_end - time_start) * 1000

        # Step 4: Postprocess the prediction to get the keypoints (model-specific)
        keypoints = self.postprocess_prediction(prediction, original_size)

        # Step 4(a): Adjust keypoints to the original image size
        if crop_bbox is not None:
            x, y, _, _ = crop_bbox
            keypoints = [(x + k[0], y + k[1], k[2]) for k in keypoints]

        return keypoints
