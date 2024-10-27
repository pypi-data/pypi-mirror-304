from typing import List

from pocketpose.registry import DETECTORS

from ..pose_estimators.base import IModel


class RTMDet(IModel):
    """Base class for RTMDet [1] models.

    The AP values are for the COCO-val2017 dataset. All models take an input image of size 256x192.

    References:
    [1] RTMDet: https://arxiv.org/abs/2212.07784

    Citing RTMDet:
    ```bibtex
    @article{lyu2022rtmdet,
        title={Rtmdet: An empirical study of designing real-time object detectors},
        author={Lyu, Chengqi and Zhang, Wenwei and Huang, Haian and Zhou, Yue and Wang, Yudong and Liu, Yanyi and Zhang, Shilong and Chen, Kai},
        journal={arXiv preprint arXiv:2212.07784},
        year={2022}
    }
    ```
    """

    def __init__(self, model_variant: str = "m", detection_threshold: float = 0.5):
        """Initialize the model.

        Args:
            model_variant (str): The model variant to use. Can be one of 't', 's', 'm', or 'l'.
        """
        super().__init__("detectors/rtmdet.json", model_variant)
        self.detection_threshold = detection_threshold

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
        detections, class_ids = prediction  # Unpack the prediction
        detections = detections[0]  # Remove the batch dimension, (Shape: Nx5)
        class_ids = class_ids[0]  # Shape: N

        # Only keep the detections that are people (class ID 0)
        detections = detections[class_ids == 0]

        # Filter out detections below the threshold
        detections = detections[detections[:, 4] > self.detection_threshold]

        # Return the processed detections
        valid_detections = []
        for detection in detections:
            x, y, w, h, score = detection

            # Scale back to the original image size
            x = x * original_size[1] / self.input_width
            y = y * original_size[0] / self.input_height
            w = w * original_size[1] / self.input_width
            h = h * original_size[0] / self.input_height

            bbox = int(x), int(y), int(w), int(h)
            valid_detections.append((bbox, score))
        return valid_detections


@DETECTORS.register_module()
class RTMDetNano(RTMDet):
    def __init__(self):
        super().__init__("nano")


@DETECTORS.register_module()
class RTMDetMedium(RTMDet):
    def __init__(self):
        super().__init__("m")
