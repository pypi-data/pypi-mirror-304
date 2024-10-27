import argparse
import sys

from pocketpose import ImageInferencer

sys.path.append("..")


def parse_args():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument("image", type=str, help="Image file path.")

    # Optional arguments
    parser.add_argument("--model", type=str, default="RTMPose_Tiny", help="Model name.")
    parser.add_argument("--radius", type=float, default=5, help="Keypoint radius.")
    parser.add_argument("--thickness", type=int, default=3, help="Link thickness.")
    parser.add_argument(
        "--kpt_thr", type=float, default=0.3, help="Keypoint threshold."
    )
    parser.add_argument(
        "--det_thr", type=float, default=0.5, help="Detection threshold."
    )
    parser.add_argument(
        "--draw_bboxes", action="store_true", help="Draw bounding boxes."
    )
    parser.add_argument(
        "--vis_out_dir", type=str, help="Visualization output directory."
    )
    parser.add_argument("--show", action="store_true", help="Show visualization.")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    image_path = args.image
    model_name = args.model
    radius = args.radius
    thickness = args.thickness
    kpt_thr = args.kpt_thr
    draw_bboxes = args.draw_bboxes
    vis_out_dir = args.vis_out_dir
    show = args.show

    # Create the PoseInferencer
    inferencer = ImageInferencer(
        pose_model=model_name,
        det_model="RTMDetMedium",
        det_thr=0.5,
        kpt_thr=kpt_thr,
        max_people=5,
        radius=radius,
        thickness=thickness,
        draw_bboxes=draw_bboxes,
        return_vis=show,
        vis_out_dir=vis_out_dir,
    )

    # Infer poses from the image file
    keypoints = inferencer.infer(image_path)

    # Print the keypoints
    print(keypoints)

    # Show the visualization image if requested
    if show:
        keypoints, kpts_vis = keypoints
        kpts_vis.show()
