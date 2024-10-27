import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple, Union

import numpy as np
from PIL import Image

from pocketpose.registry import DETECTORS, POSE_ESTIMATORS, VISUALIZERS


class ImageInferencer:
    """
    ImageInferencer provides a unified interface to infer poses from images.

    Args:
        pose_model (str): Name of the pose estimation model to use.
        det_model (Optional[str]): Name of the detection model to use. If None, assumes the pose model can detect persons.
        kpt_thr (float): Keypoint score threshold. Keypoints with scores exceeding this will be displayed.
        det_thr (float): Detection confidence threshold.
        max_people (int): Maximum number of people to detect. -1 for no limit.
        show_bboxes (bool): Whether to display bounding boxes of detected persons.
        joint_radius (float): Radius of keypoints in visualization.
        linewidth (int): Thickness of links in visualization.
        return_vis (bool): Whether to return visualization images along with keypoints.
        vis_out_dir (Optional[str]): Directory to save visualization images. If None, images are not saved.
        num_workers (int): Number of worker threads for parallel processing.
    """

    def __init__(
        self,
        pose_model: str,
        det_model: Optional[str] = None,
        kpt_thr: float = 0.3,
        det_thr: float = 0.5,
        max_people: int = -1,
        draw_bboxes: bool = False,
        radius: float = 5.0,
        thickness: int = 3,
        return_vis: bool = False,
        vis_out_dir: Optional[str] = None,
        num_workers: int = 4,
    ):
        # Initialize pose estimator
        try:
            self.pose_estimator = POSE_ESTIMATORS.build(pose_model)
            self.model_name = self.pose_estimator.__class__.__name__
        except Exception as e:
            raise ValueError(f"Failed to build pose estimator '{pose_model}': {e}")

        # Initialize detector if provided
        self.detector = None
        if det_model:
            try:
                self.detector = DETECTORS.build(det_model)
                self.detector.detection_threshold = det_thr
            except Exception as e:
                raise ValueError(f"Failed to build detector '{det_model}': {e}")

        self.max_people = max_people

        # Initialize visualizer
        try:
            self.visualizer = VISUALIZERS.build(
                "PoseVisualizer",
                self.pose_estimator.keypoints_type,
                radius=radius,
                thickness=thickness,
                kpt_thr=kpt_thr,
                draw_bboxes=draw_bboxes,
            )
        except Exception as e:
            raise ValueError(f"Failed to build visualizer: {e}")

        self.return_vis = return_vis
        self.vis_out_dir = vis_out_dir
        self.last_inference_duration_ms = 0
        self.num_workers = num_workers

        # Create visualization output directory if needed
        if self.vis_out_dir:
            os.makedirs(self.vis_out_dir, exist_ok=True)

    def _save_visualization(
        self,
        image: np.ndarray,
        keypoints: List,
        detections: Optional[List] = None,
        image_path: str = "",
    ) -> Image.Image:
        """
        Generate and save the visualization image.

        Args:
            image (np.ndarray): The original image.
            keypoints (List): List of keypoints.
            detections (Optional[List]): List of detections if available.
            image_path (str): Path to the original image.

        Returns:
            PIL.Image.Image: The visualization image.
        """
        kpts_vis = self.visualizer.visualize(image, keypoints, detections)
        if self.vis_out_dir:
            filename = os.path.splitext(os.path.basename(image_path))[0]
            save_path = os.path.join(
                self.vis_out_dir, f"{filename}_{self.model_name}.jpg"
            )
            kpts_vis.save(save_path)
        return kpts_vis

    def infer_multi(
        self, image: np.ndarray, image_path: str
    ) -> Union[List, Tuple[List, Image.Image]]:
        """
        Infer poses for multiple people in an image.

        Args:
            image (np.ndarray): The image to process.
            image_path (str): Path to the image file.

        Returns:
            Union[List, Tuple[List, Image.Image]]: List of keypoints or tuple with keypoints and visualization.
        """
        # Detect people in the image
        start_time = time.time()
        detections = self.detector(image) if self.detector else []
        n_detections = len(detections)
        detection_time = (time.time() - start_time) * 1000  # in ms

        if n_detections == 0:
            self.last_inference_duration_ms = detection_time
            return [] if not self.return_vis else ([], None)

        # Sort detections by confidence and keep top max_people
        if self.max_people > 0:
            detections = sorted(detections, key=lambda x: x[1], reverse=True)[
                : self.max_people
            ]
        else:
            detections = sorted(detections, key=lambda x: x[1], reverse=True)

        # Parallel pose estimation
        keypoints = []
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [
                executor.submit(self.pose_estimator, image, bbox)
                for bbox, _ in detections
            ]
            for future in as_completed(futures):
                try:
                    kp = future.result()
                    keypoints.append(kp)
                except Exception as e:
                    keypoints.append(None)  # or handle accordingly

        inference_time = (time.time() - start_time) * 1000  # in ms
        self.last_inference_duration_ms = inference_time

        if self.return_vis or self.vis_out_dir:
            kpts_vis = self._save_visualization(
                image, keypoints, detections, image_path
            )
            if self.return_vis:
                return keypoints, kpts_vis

        return keypoints

    def infer(self, image_path: str) -> Union[List, Tuple[List, Image.Image]]:
        """
        Infer poses from an image file.

        Args:
            image_path (str): Path to the image file.

        Returns:
            Union[List, Tuple[List, Image.Image]]: List of keypoints or tuple with keypoints and visualization.
        """
        try:
            image = Image.open(image_path).convert("RGB")
            image = np.array(image)
        except Exception as e:
            raise ValueError(f"Failed to open image '{image_path}': {e}")

        if self.detector:
            return self.infer_multi(image, image_path)

        # Single pose estimation
        start_time = time.time()
        keypoints = self.pose_estimator(image)
        inference_time = (time.time() - start_time) * 1000  # in ms
        self.last_inference_duration_ms = inference_time

        if self.return_vis or self.vis_out_dir:
            kpts_vis = self.visualizer.visualize(image, keypoints)
            if self.vis_out_dir:
                filename = os.path.splitext(os.path.basename(image_path))[0]
                save_path = os.path.join(
                    self.vis_out_dir, f"{filename}_{self.model_name}.jpg"
                )
                kpts_vis.save(save_path)
            if self.return_vis:
                return keypoints, kpts_vis

        return keypoints
