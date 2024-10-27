from pocketpose.registry import DATASETS

from .base import Skeleton


@DATASETS.register_module(name="coco")
class COCOSkeleton(Skeleton):
    def __init__(self) -> None:
        super().__init__(
            "coco",
            nodes={
                0: "nose",
                1: "left_eye",
                2: "right_eye",
                3: "left_ear",
                4: "right_ear",
                5: "left_shoulder",
                6: "right_shoulder",
                7: "left_elbow",
                8: "right_elbow",
                9: "left_wrist",
                10: "right_wrist",
                11: "left_hip",
                12: "right_hip",
                13: "left_knee",
                14: "right_knee",
                15: "left_ankle",
                16: "right_ankle",
            },
            edges=[
                (0, 1),
                (0, 2),
                (1, 2),  # Eyes
                (1, 3),
                (2, 4),  # Ears
                (3, 5),
                (4, 6),
                (5, 6),  # Head and Shoulders
                (6, 12),
                (5, 11),
                (11, 12),  # Trunk
                (5, 7),
                (7, 9),  # Right Arm
                (6, 8),
                (8, 10),  # Left Arm
                (11, 13),
                (13, 15),  # Right Leg
                (12, 14),
                (14, 16),  # Left Leg
            ],
        )
