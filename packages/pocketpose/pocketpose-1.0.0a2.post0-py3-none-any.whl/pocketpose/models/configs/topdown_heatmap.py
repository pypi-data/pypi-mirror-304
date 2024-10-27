# =====================================
# Top-Down Pose Estimation (Two-Stage)
# -------------------------------------
# Heatmap Regression
[
    # -- 1) AlexNet
    dict(
        name="td-hm_alexnet_coco-256x192",
        pretty_name="AlexNet",
        input_size=[256, 192, 3],
        skeleton="coco",
        runtime="onnx",
        download=dict(
            float32="https://drive.google.com/file/d/1ctPyDGVRCzW5ckIefkGmrBfyyT9BqJkZ/view?usp=sharing",
        ),
        source=dict(
            name="MMPose",
            url="https://download.openmmlab.com/mmpose/top_down/alexnet/alexnet_coco_256x192-a7b1fd15_20200727.pth",
            code="https://github.com/open-mmlab/mmpose/tree/dev-1.x/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_alexnet_8xb64-210e_coco-256x192.py",
        ),
        notes="Converted to ONNX from MMPose Model Zoo using MMDeploy.",
        license="Apache-2.0 License",
    ),
    # -- 2) ShuffleNet (V1, V2)
    dict(
        name="td-hm_shufflenetv1_coco-256x192",
        pretty_name="ShuffleNetV1",
        input_size=[256, 192, 3],
        skeleton="coco",
        runtime="onnx",
        download=dict(
            float32="https://drive.google.com/file/d/1Vij-b_P1T4lf58bMygpB3tsU66INsWqQ/view?usp=sharing",
        ),
        source=dict(
            name="MMPose",
            url="https://download.openmmlab.com/mmpose/v1/body_2d_keypoint/topdown_heatmap/coco/td-hm_shufflenetv1_8xb64-210e_coco-256x192-7a7ea4f4_20221013.pth",
            code="https://github.com/open-mmlab/mmpose/tree/dev-1.x/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_shufflenetv1_8xb64-210e_coco-256x192.py",
        ),
        notes="Converted to ONNX from MMPose Model Zoo using MMDeploy.",
        license="Apache-2.0 License",
    ),
    dict(
        name="td-hm_shufflenetv2_coco-256x192",
        pretty_name="ShuffleNetV2",
        input_size=[256, 192, 3],
        skeleton="coco",
        runtime="onnx",
        download=dict(
            float32="https://drive.google.com/file/d/1oS1xEVeRC05wgjIbxovlh3HJYLv7_nAZ/view?usp=sharing",
        ),
        source=dict(
            name="MMPose",
            url="https://download.openmmlab.com/mmpose/v1/body_2d_keypoint/topdown_heatmap/coco/td-hm_shufflenetv2_8xb64-210e_coco-256x192-51fb931e_20221014.pth",
            code="https://github.com/open-mmlab/mmpose/tree/dev-1.x/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_shufflenetv2_8xb64-210e_coco-256x192.py",
        ),
        notes="Converted to ONNX from MMPose Model Zoo using MMDeploy.",
        license="Apache-2.0 License",
    ),
    # -- 3) MobileNets (V2)
    dict(
        name="td-hm_mobilenetv2_coco-256x192",
        pretty_name="MobileNetV2",
        input_size=[256, 192, 3],
        skeleton="coco",
        runtime="onnx",
        download=dict(
            float32="https://drive.google.com/file/d/11AJy9eKFTeyV2XP4xtiCzw8cK8EVtHBV/view?usp=sharing",
        ),
        source=dict(
            name="MMPose",
            url="https://download.openmmlab.com/mmpose/v1/body_2d_keypoint/topdown_heatmap/coco/td-hm_mobilenetv2_8xb64-210e_coco-256x192-55a04c35_20221016.pth",
            code="https://github.com/open-mmlab/mmpose/tree/dev-1.x/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_mobilenetv2_8xb64-210e_coco-256x192.py",
        ),
        notes="Converted to ONNX from MMPose Model Zoo using MMDeploy.",
        license="Apache-2.0 License",
    ),
    # -- 4) LiteHRNet (18, 30)
    dict(
        name="td-hm_litehrnet-18_coco-256x192",
        pretty_name="LiteHRNet-18",
        input_size=[256, 192, 3],
        skeleton="coco",
        runtime="onnx",
        download=dict(
            float32="https://drive.google.com/file/d/1AhId90baINsI3AI1TocD3nZISQqa1FRU/view?usp=sharing",
        ),
        source=dict(
            name="MMPose",
            url="https://download.openmmlab.com/mmpose/top_down/litehrnet/litehrnet18_coco_256x192-6bace359_20211230.pth",
            code="https://github.com/open-mmlab/mmpose/tree/dev-1.x/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_litehrnet-18_8xb64-210e_coco-256x192.py",
        ),
        notes="Converted to ONNX from MMPose Model Zoo using MMDeploy.",
        license="Apache-2.0 License",
    ),
    dict(
        name="td-hm_litehrnet-30_coco-256x192",
        pretty_name="LiteHRNet-30",
        input_size=[256, 192, 3],
        skeleton="coco",
        runtime="onnx",
        download=dict(
            float32="https://drive.google.com/file/d/1C9EUxIy-68V89lcw9rs1tXHxj25DC6mK/view?usp=sharing",
        ),
        source=dict(
            name="MMPose",
            url="https://download.openmmlab.com/mmpose/top_down/litehrnet/litehrnet30_coco_256x192-4176555b_20210626.pth",
            code="https://github.com/open-mmlab/mmpose/tree/dev-1.x/configs/body_2d_keypoint/topdown_heatmap/coco/td-hm_litehrnet-30_8xb64-210e_coco-256x192.py",
        ),
        notes="Converted to ONNX from MMPose Model Zoo using MMDeploy.",
        license="Apache-2.0 License",
    ),
]
