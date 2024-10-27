from typing import List

from pocketpose.models.decoder import SimCCDecoder
from pocketpose.registry import POSE_ESTIMATORS

from .base import IModel


class TopdownCCModel(IModel):
    """Base class for SimCC [1] models.

    [1] SimCC: https://arxiv.org/abs/2107.03332
    """

    def __init__(self, model_variant: str, **kwargs):
        super().__init__("topdown_coord_cls.json", model_variant, **kwargs)
        self.decoder = SimCCDecoder()

    def process_image(self, image):
        image = image.transpose(0, 3, 1, 2)  # NHWC -> NCHW
        return image / 255.0  # [0, 255] -> [0, 1]

    def postprocess_prediction(self, prediction, original_size) -> List[List[float]]:
        return self.decoder.decode(prediction, tuple(original_size))


@POSE_ESTIMATORS.register_module()
class SimCCMobileNetV2(TopdownCCModel):
    def __init__(self, **kwargs):
        super().__init__("mobilenetv2_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class SimCCViPNAS_MobileNetV3(TopdownCCModel):
    def __init__(self, **kwargs):
        super().__init__("vipnas-mobilenetv3_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class SimCCResNet50(TopdownCCModel):
    def __init__(self, **kwargs):
        super().__init__("resnet50_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class RTMPose_Tiny(TopdownCCModel):
    def __init__(self, **kwargs):
        super().__init__("rtmpose-t_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class RTMPose_Small(TopdownCCModel):
    def __init__(self, **kwargs):
        super().__init__("rtmpose-s_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class RTMPose_Medium(TopdownCCModel):
    def __init__(self, **kwargs):
        super().__init__("rtmpose-m_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class RTMPose_Large(TopdownCCModel):
    def __init__(self, **kwargs):
        super().__init__("rtmpose-l_coco", **kwargs)


@POSE_ESTIMATORS.register_module()
class RTMW_Medium(TopdownCCModel):
    def __init__(self, **kwargs):
        super().__init__("rtmw-m_coco-wholebody", **kwargs)
