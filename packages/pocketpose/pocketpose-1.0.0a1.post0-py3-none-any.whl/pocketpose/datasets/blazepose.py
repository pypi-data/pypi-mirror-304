from pocketpose.registry import DATASETS

from .base import Skeleton


@DATASETS.register_module(name="blazepose")
class BlazePoseSkeleton(Skeleton):
    def __init__(self) -> None:
        super().__init__(
            "blazepose",
            nodes={
                0: "nose",
                1: "left_inner_eye",
                2: "left_eye",
                3: "left_outer_eye",
                4: "right_inner_eye",
                5: "right_eye",
                6: "right_outer_eye",
                7: "left_ear",
                8: "right_ear",
                9: "mouth_left",
                10: "mouth_right",
                11: "left_shoulder",
                12: "right_shoulder",
                13: "left_elbow",
                14: "right_elbow",
                15: "left_wrist",
                16: "right_wrist",
                17: "left_pinky_1",
                18: "right_pinky_1",
                19: "left_index_1",
                20: "right_index_1",
                21: "left_thumb_2",
                22: "right_thumb_2",
                23: "left_hip",
                24: "right_hip",
                25: "left_knee",
                26: "right_knee",
                27: "left_ankle",
                28: "right_ankle",
                29: "left_heel",
                30: "right_heel",
                31: "left_foot_index",
                32: "right_foot_index",
                33: "body_center",
                34: "forehead",
                35: "left_thumb",
                36: "left_hand",
                37: "right_thumb",
                38: "right_hand",
            },
            edges=[
                (0, 2),
                (1, 2),
                (2, 3),
                (0, 5),
                (4, 5),
                (5, 6),  # Eyes
                (3, 7),
                (6, 8),  # Ears
                (9, 10),  # Mouth
                (11, 12),  # Shoulders
                (12, 24),
                (11, 23),
                (23, 24),  # Trunk
                (11, 13),
                (13, 15),
                (15, 17),
                (15, 19),
                (15, 21),
                (17, 19),  # Right Arm
                (12, 14),
                (14, 16),
                (16, 18),
                (16, 20),
                (16, 22),
                (18, 20),  # Left Arm
                (23, 25),
                (25, 27),
                (27, 29),
                (27, 31),
                (29, 31),  # Right Leg
                (24, 26),
                (26, 28),
                (28, 30),
                (28, 32),
                (30, 32),  # Left Leg
            ],
        )

    def get_coco_subset(self, skeleton):
        return [
            skeleton[i]
            for i in [0, 2, 5, 7, 8, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
        ]
