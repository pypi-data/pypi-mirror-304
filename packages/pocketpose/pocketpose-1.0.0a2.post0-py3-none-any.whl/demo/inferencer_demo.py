import argparse
import sys

from pocketpose import ImageInferencer

sys.path.append("..")


def parse_args():
    parser = argparse.ArgumentParser(description="Pose Estimation Demo Script")

    # Required arguments
    parser.add_argument("image_path", type=str, help="Path to the input image file.")

    # Optional arguments
    parser.add_argument(
        "--pose_model",
        type=str,
        default="RTMPose_Large",
        help="Name of the pose estimation model.",
    )
    parser.add_argument(
        "--det_model",
        type=str,
        default="RTMDetMedium",
        help="Name of the pose estimation model.",
    )
    
    parser.add_argument(
        "--radius",
        type=float,
        default=5.0,
        help="Radius of keypoints in visualization.",
    )
    parser.add_argument(
        "--thickness",
        type=int,
        default=3,
        help="Thickness of the links between keypoints.",
    )
    parser.add_argument(
        "--kpt_thr",
        type=float,
        default=0.3,
        help="Threshold for keypoint confidence scores.",
    )
    parser.add_argument(
        "--det_thr",
        type=float,
        default=0.5,
        help="Threshold for detection confidence scores.",
    )
    parser.add_argument(
        "--draw_bboxes",
        action="store_true",
        help="Flag to draw bounding boxes around detected persons.",
    )
    parser.add_argument(
        "--max_people",
        type=int,
        default=5,
        help="Maximum people to detect",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default=None,
        help="Path to save the visualization image.",
    )
    parser.add_argument(
        "--show", action="store_true", help="Flag to display the visualization image."
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Define visualization configuration
    visualization_config = {
        "kpt_thr": args.kpt_thr,
        "radius": args.radius,
        "thickness": args.thickness,
        "draw_bboxes": args.draw_bboxes,
    }

    # Initialize the ImageInferencer
    inferencer = ImageInferencer(
        pose_model=args.pose_model,
        det_model=args.det_model,
        det_thr=args.det_thr,
        max_people=args.max_people,
        visualization_config=visualization_config,
    )

    # Perform pose estimation
    inference_result = inferencer.infer(
        image_path=args.image_path,
        visualize=args.show,
        return_vis=args.show,
        save_path=args.save_path,
    )

    # Handle the inference result
    if args.show:
        keypoints, vis_image = inference_result
        print(keypoints)
        vis_image.show()
    else:
        keypoints = inference_result
        print(keypoints)


if __name__ == "__main__":
    main()
