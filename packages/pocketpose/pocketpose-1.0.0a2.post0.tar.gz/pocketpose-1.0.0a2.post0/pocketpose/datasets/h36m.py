from pocketpose.registry import DATASETS

from .base import Skeleton


@DATASETS.register_module(name="h36m")
class H36MSkeleton(Skeleton):
    def __init__(self) -> None:
        super().__init__(
            "h36m",
            nodes={
                0: "pelvis",
                1: "left_hip",
                2: "left_knee",
                3: "left_ankle",
                4: "right_hip",
                5: "right_knee",
                6: "right_ankle",
                7: "spine_mid",
                8: "neck",
                9: "chin",
                10: "nose",
                11: "right_shoulder",
                12: "right_elbow",
                13: "right_wrist",
                14: "left_shoulder",
                15: "left_elbow",
                16: "left_wrist",
            },
            edges=[
                (3, 2),
                (2, 1),
                (1, 0),
                (0, 4),
                (4, 5),
                (5, 6),
                (0, 7),
                (7, 8),
                (8, 9),
                (9, 10),
                (8, 11),
                (11, 12),
                (12, 13),
                (8, 14),
                (14, 15),
                (15, 16),
            ],
        )
