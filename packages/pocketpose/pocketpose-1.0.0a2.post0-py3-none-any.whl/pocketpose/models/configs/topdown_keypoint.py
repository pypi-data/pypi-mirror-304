# =====================================
# Top-Down Pose Estimation (Two-Stage)
# -------------------------------------
# Keypoint Regression
[
    # -- 1) BlazePose (Lite, Full, Heavy)
    dict(
        name="td-kp_blazepose-lite_blazepose-256x256",
        pretty_name="BlazePose Lite",
        input_size=[256, 256, 3],
        skeleton="blazepose",
        runtime="mediapipe",
        download=dict(
            float16="https://drive.google.com/file/d/1lTYBuK2K70Od7c_UjJq33Ap3Wvt_5w9I/view?usp=sharing",
        ),
        source=dict(
            name="MediaPipe",
            url="https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task",
            code="https://github.com/google/mediapipe",
        ),
        notes="",
        license="Apache-2.0 License",
    ),
    dict(
        name="td-kp_blazepose-full_blazepose-256x256",
        pretty_name="BlazePose Full",
        input_size=[256, 256, 3],
        skeleton="blazepose",
        runtime="mediapipe",
        download=dict(
            float16="https://drive.google.com/file/d/1ckRy3I5t_vRnPzTrMyl1Ou4UcIH64xiS/view?usp=sharing",
        ),
        source=dict(
            name="MediaPipe",
            url="https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task",
            code="https://github.com/google/mediapipe",
        ),
        notes="",
        license="Apache-2.0 License",
    ),
    dict(
        name="td-kp_blazepose-heavy_blazepose-256x256",
        pretty_name="BlazePose Heavy",
        input_size=[256, 256, 3],
        skeleton="blazepose",
        runtime="mediapipe",
        download=dict(
            float16="https://drive.google.com/file/d/1LnzU3vq9ezhf3KitNLkV8zkwtXxN8vf3/view?usp=sharing",
        ),
        source=dict(
            name="MediaPipe",
            url="https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task",
            code="https://github.com/google/mediapipe",
        ),
        notes="",
        license="Apache-2.0 License",
    ),
    # -- 2) MoveNet (Lightning, Thunder)
    dict(
        name="td-kp_movenet-lightning_coco-192x192",
        pretty_name="MoveNet Lightning",
        input_size=[192, 192, 3],
        skeleton="coco",
        runtime="tflite",
        download=dict(
            float32="https://drive.google.com/file/d/17E_QH9_8bt_DCi2ey08CPDT3-AJGM81P/view?usp=sharing",
            float16="https://drive.google.com/file/d/1Th9y2AOdQVKhM9OJ65EIsgAHerDtxSpj/view?usp=sharing",
            int8="https://drive.google.com/file/d/1JbVRFrCvrmC8tE7VX7_v1AKqI12gEUVE/view?usp=sharing",
        ),
        source=dict(
            name="TensorFlow Hub",
            url="",
            code="",
        ),
        notes="",
        license="Apache-2.0 License",
    ),
    dict(
        name="td-kp_movenet-thunder_coco-256x256",
        pretty_name="MoveNet Thunder",
        input_size=[256, 256, 3],
        skeleton="coco",
        runtime="tflite",
        download=dict(
            float32="https://drive.google.com/file/d/1NHIO9hU-8YLreT9TFyMqgjXJWWPMWNwi/view?usp=sharing",
            float16="https://drive.google.com/file/d/1qzbwGjsZ-HHUmr3xFGHEUhsjrU2ewsZ8/view?usp=sharing",
            int8="https://drive.google.com/file/d/1ZAhBmrm6zu7R1k1AknXT1dsXryu6UMjd/view?usp=sharing",
        ),
        source=dict(
            name="TensorFlow Hub",
            url="",
            code="",
        ),
        notes="",
        license="Apache-2.0 License",
    ),
]
