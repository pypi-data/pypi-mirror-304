import os

import cv2

from pocketpose.registry import DETECTORS

from .image_inferencer import ImageInferencer


class VideoInferencer(ImageInferencer):
    def __init__(
        self,
        model_name: str,
        detector_name: str = "RTMDetMedium",
        detection_threshold: float = 0.3,
        **kwargs,
    ):
        super().__init__(model_name, **kwargs)
        self.detector = DETECTORS.build(detector_name)
        self.detector.detection_threshold = detection_threshold

        # Tracking-related attributes
        self.bbox = None  # Bounding box of the selected person
        self.tracker = None  # Tracker object
        self.initialized = False  # Whether the tracker has been initialized

    def check_valid(self, bbox):
        x, y, w, h = bbox
        return x >= 0 and y >= 0 and w > 0 and h > 0

    def initialize_tracker(self, frame, bbox):
        if not self.check_valid(bbox):
            return

        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(frame, bbox)
        self.bbox = bbox
        self.initialized = True

    def reset_tracker(self):
        self.tracker = None
        self.bbox = None
        self.initialized = False

    def update_bbox(self, frame):
        # Update the bounding box based on the tracker
        success, bbox = self.tracker.update(frame)
        if success and self.check_valid(bbox):
            self.bbox = bbox
            print(f"Updated bbox: {bbox}")
        return success

    def infer(self, image_path: str):
        keypoints = None
        kpts_vis = None
        if not self.initialized:
            # Run detection and let user select which person to track
            detections = self.detector(image_path)

            # If no detections, return an empty list
            if detections:
                # Select the detection with the highest confidence
                # bbox, _ = max(detections, key=lambda x: x[1])
                bbox = detections[0][0]
                self.initialize_tracker(image_path, bbox)
        else:
            # Update the bounding box with the tracker
            if self.update_bbox(image_path):
                try:
                    keypoints = self.model(image_path, self.bbox)
                    self.last_inference_duration_ms = (
                        self.model.last_inference_duration_ms
                    )
                except Exception as e:
                    print(f"Error during inference: {e}")
                    self.reset_tracker()
            else:
                # Handle tracking failure
                self.reset_tracker()

            if self.return_vis or self.vis_out_dir is not None:
                kpts_vis = self.visualizer.visualize(image_path, keypoints, self.bbox)
                if self.vis_out_dir is not None:
                    os.makedirs(self.vis_out_dir, exist_ok=True)
                    kpts_vis.save(
                        os.path.join(
                            self.vis_out_dir,
                            os.path.splitext(os.path.basename(image_path))[0]
                            + "_"
                            + self.model_name
                            + ".jpg",
                        )
                    )
                return (keypoints, kpts_vis)
            else:
                return keypoints
