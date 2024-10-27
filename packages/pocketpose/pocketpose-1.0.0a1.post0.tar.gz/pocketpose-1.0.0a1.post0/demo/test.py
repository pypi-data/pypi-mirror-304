import pocketpose as pp


def main():
    inferencer = pp.ImageInferencer(
        pose_model="RTMPose_Large",
        det_model="RTMDetMedium",
        det_thr=0.5,
        kpt_thr=0.2,
        return_vis=True,
        max_people=1,
    )
    keypoints, vis = inferencer.infer("data/demo/person08.jpg")
    print(f"Found {len(keypoints)} people in the image.")

    # Print time taken for inference
    print(
        f"Time taken for inference: {(inferencer.last_inference_duration_ms/1000):.2f} seconds"
    )

    # Write the visualization image to disk
    vis.save("data/demo/person08_pose.jpg")


if __name__ == "__main__":
    main()
