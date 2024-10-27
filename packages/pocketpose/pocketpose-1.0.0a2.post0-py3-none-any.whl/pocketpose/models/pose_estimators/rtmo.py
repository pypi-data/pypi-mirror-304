import os
from typing import List

from pocketpose.core.config import load_cfg
from pocketpose.models.decoder import SimCCDecoder
from pocketpose.models.interfaces import ONNXModel
from pocketpose.registry import POSE_ESTIMATORS


class RTMO(ONNXModel):
    """Base class for RTMO [1] models.

    [1] RTMO:

    Citing RTMO:
    ```bibtex
    @article{jiang2023rtmpose,
        title={RTMPose: Real-Time Multi-Person Pose Estimation based on MMPose},
        author={Jiang, Tao and Lu, Peng and Zhang, Li and Ma, Ningsheng and Han, Rui and Lyu, Chengqi and Li, Yining and Chen, Kai},
        journal={arXiv preprint arXiv:2303.07399},
        year={2023}
    }
    ```
    """

    def __init__(self, model_variant: str = "m"):
        """Initialize the model.

        Args:
            model_variant (str): The model variant to use. Can be one of 't', 's', 'm', or 'l'.
        """
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cfg_file = os.path.join(root_dir, "../configs/rtmo.json")
        cfg = load_cfg(cfg_file, model_variant)
        self.name = cfg["name"]
        self.description = cfg["description"]
        self.paper = cfg["paper"]
        self.type = cfg["type"]
        self.decoder = SimCCDecoder()
        super().__init__(
            cfg["cache_path"],
            cfg["url"],
            keypoints_type=cfg["keypoints"],
            input_size=cfg["input_size"],
        )

    def process_image(self, image):
        """Preprocess the image for the model.

        RTMPose expects the image to be in the format (batch, channels, height, width), and
        the values to be in the range [0, 1].

        Args:
            image (np.ndarray): The image to preprocess.

        Returns:
            np.ndarray: The preprocessed image.
        """
        image = image.transpose(0, 3, 1, 2)  # NHWC -> NCHW
        return image / 255.0  # [0, 255] -> [0, 1]

    def postprocess_prediction(self, prediction, original_size) -> List[List[float]]:
        return self.decoder.decode(prediction, tuple(original_size))


@POSE_ESTIMATORS.register_module()
class RTMOS(RTMO):
    def __init__(self):
        super().__init__("s")
