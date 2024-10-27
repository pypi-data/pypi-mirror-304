from pocketpose.registry import DATASETS

from .base import Skeleton


@DATASETS.register_module(name="mpii")
class MPIISkeleton(Skeleton):
    def __init__(self) -> None:
        super().__init__(
            "mpii",
            nodes={
                0: "right_ankle",
                1: "right_knee",
                2: "right_hip",
                3: "left_hip",
                4: "left_knee",
                5: "left_ankle",
                6: "pelvis",
                7: "thorax",
                8: "upper_neck",
                9: "head_top",
                10: "right_wrist",
                11: "right_elbow",
                12: "right_shoulder",
                13: "left_shoulder",
                14: "left_elbow",
                15: "left_wrist",
            },
            edges=[
                (0, 1),
                (1, 2),
                (2, 6),
                (3, 6),
                (3, 4),
                (4, 5),  # Legs
                (6, 7),
                (7, 8),
                (8, 9),  # Body
                (10, 11),
                (11, 12),
                (12, 7),  # Right Arm
                (7, 13),
                (13, 14),
                (14, 15),  # Left Arm
            ],
        )
