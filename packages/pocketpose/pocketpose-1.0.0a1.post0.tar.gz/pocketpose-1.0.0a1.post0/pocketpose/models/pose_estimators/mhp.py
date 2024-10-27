import numpy as np
from scipy.special import softmax

from pocketpose.models.decoder import HeatmapDeocder
from pocketpose.models.interfaces import TFLiteModel
from pocketpose.registry import POSE_ESTIMATORS


class MHP(TFLiteModel):
    """Base class for the MoveNet models.

    MoveNet is a lightweight pose estimation model developed by Google Research
    that runs on mobile devices. It uses a lightweight MobileNetV2 backbone and
    a Feature Pyramid Network (FPN) decoder together with CenterNet-style keypoint
    prediction heads. The model is trained on the COCO dataset and can detect 17
    keypoints.

    For more information, see the following links:
    - https://www.tensorflow.org/hub/tutorials/movenet
    - https://blog.tensorflow.org/2021/05/next-generation-pose-detection-with-movenet-and-tensorflowjs.html
    """

    def __init__(self, model_path: str, model_url: str, input_size: tuple):
        """Initialize the model.

        Args:
            model_path (str): Path to the model file.
            model_url (str): URL to download the model from.
            input_size (tuple): Input size of the model as (width, height, channels).
        """
        super().__init__(
            model_path,
            model_url,
            keypoints_type="coco",
            input_size=input_size,
            output_type="keypoints",
        )
        self.num_keypoints = 21
        self.output_depth = 672 // self.num_keypoints
        self.output_width = 32
        self.output_height = 32
        self.decoder = HeatmapDeocder()

    def postprocess_prediction(self, prediction, original_size):
        output = prediction.reshape(
            (
                1,
                self.output_height,
                self.output_width,
                self.num_keypoints,
                self.output_depth,
            )
        )
        output = output.max(axis=4)  # Shape: (1, 32, 32, 21)
        output = output.transpose((0, 3, 1, 2))  # Shape: (1, 21, 32, 32)
        return self.decoder.decode(output.squeeze(), original_size)

        # heatmaps = prediction.reshape((-1, self.num_keypoints, self.output_depth * self.output_height * self.output_width))
        # heatmaps = softmax(heatmaps, 2)

        # scores = np.squeeze(np.max(heatmaps, 2)) # Ref: https://github.com/mks0601/3DMPPE_POSENET_RELEASE/issues/47

        # heatmaps = heatmaps.reshape((-1, self.num_keypoints, self.output_depth, self.output_height, self.output_width)) # 3D heatmap
        # print("Heatmaps shape:", heatmaps.shape)
        # accu_x = heatmaps.sum(axis=(2,3))
        # accu_y = heatmaps.sum(axis=(2,4))
        # accu_z = heatmaps.sum(axis=(3,4))
        # print("X shape:", accu_x.shape)
        # print("Y shape:", accu_y.shape)
        # print("Z shape:", accu_z.shape)

        # accu_x = accu_x * np.arange(self.output_width, dtype=np.float32)
        # accu_y = accu_y * np.arange(self.output_height, dtype=np.float32)
        # accu_z = accu_z * np.arange(self.output_depth, dtype=np.float32)

        # accu_x = accu_x.sum(axis=2, keepdims=True)
        # accu_y = accu_y.sum(axis=2, keepdims=True)
        # accu_z = accu_z.sum(axis=2, keepdims=True)

        # print("X' shape:", accu_x.shape)
        # print("Y' shape:", accu_y.shape)
        # print("Z' shape:", accu_z.shape)

        # scores2 = []
        # for i in range(self.num_keypoints):
        #     scores2.append(heatmaps.sum(axis=2)[0, i, int(accu_y[0,i,0]), int(accu_x[0,i,0])])

        # accu_x = accu_x / self.output_width
        # accu_y = accu_y / self.output_height
        # accu_z = accu_z / self.output_depth * 2 - 1

        # # print range of x, y, z
        # print(accu_x.min(), accu_x.max())
        # print(accu_y.min(), accu_y.max())
        # print(accu_z.min(), accu_z.max())
        # print()

        # coord_out = np.squeeze(np.concatenate((accu_x, accu_y, accu_z), axis=2))

        # pose_2d = coord_out[:,:2]
        # pose_2d[:,0] = pose_2d[:,0] * original_size[1] # + bbox[0]
        # pose_2d[:,1] = pose_2d[:,1] * original_size[0] # + bbox[1]

        # keypoints = np.zeros((self.num_keypoints, 3))
        # keypoints[:, :2] = pose_2d.astype(int)
        # keypoints[:, 2] = scores2

        # print(keypoints[:5])

        # # joint_depth = coord_out[:,2]*1000 + abs_depth

        # return keypoints.tolist()  # (17, 3) as (x, y, score)


@POSE_ESTIMATORS.register_module()
class MHPFP16(MHP):
    """MoveNet Lightning model.

    The Lightning model is the smallest MoveNet model and is intended for
    latency-critical applications.
    """

    def __init__(self):
        super().__init__(
            "../../.cache/models/body3d/mhp/tflite/mobilehumanpose_fp16.tflite",
            "",  # TODO: Add model URL
            (256, 256, 3),
        )
