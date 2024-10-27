from pocketpose.registry import DATASETS

from .base import Skeleton


@DATASETS.register_module(name="mhp")
class MHPSkeleton(Skeleton):
    def __init__(self) -> None:
        super().__init__(
            "mhp",
            nodes={
                0: "Head_top",
                1: "Thorax",
                2: "R_Shoulder",
                3: "R_Elbow",
                4: "R_Wrist",
                5: "L_Shoulder",
                6: "L_Elbow",
                7: "L_Wrist",
                8: "R_Hip",
                9: "R_Knee",
                10: "R_Ankle",
                11: "L_Hip",
                12: "L_Knee",
                13: "L_Ankle",
                14: "Pelvis",
                15: "Spine",
                16: "Head",
                17: "R_Hand",
                18: "L_Hand",
                19: "R_Toe",
                20: "L_Toe",
            },
            edges=[
                (0, 16),
                (16, 1),
                (1, 15),
                (15, 14),
                (14, 8),
                (14, 11),
                (8, 9),
                (9, 10),
                (10, 19),
                (11, 12),
                (12, 13),
                (13, 20),
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 17),
                (1, 5),
                (5, 6),
                (6, 7),
                (7, 18),
            ],
        )
