import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple, Union

import numpy as np
from PIL import Image

from pocketpose.registry import DETECTORS, POSE_ESTIMATORS, VISUALIZERS


class ImageInferencer:
    """
    Provides a unified interface for performing pose estimation on images.

    This class supports both single-stage and two-stage (top-down) pose estimation approaches.
    It allows for parallel processing of multiple detections and offers visualization capabilities.

    Args:
        pose_model (str): The identifier of the pose estimation model to use. Defaults to `RTMPose_Large`.
        det_model (Optional[str], optional): The identifier of the detection model to use. Defaults to `RTMDetMedium`.
            If `None`, the pose model is assumed to have built-in person detection capabilities.
            Defaults to `None`.
        det_thr (float, optional): Confidence threshold for detections. Detections with scores below
            this threshold will be discarded. Defaults to `0.5`.
        max_people (int, optional): Maximum number of people to detect in an image.
            Set to `-1` for no limit. Defaults to `-1`.
        num_workers (int, optional): Number of worker threads for parallel pose estimation.
            Defaults to `4`.
        visualization_config (dict, optional): Configuration parameters for visualization.
            Expected keys:
                - `kpt_thr` (float): Keypoint score threshold for visualization.
                - `radius` (float): Radius of keypoints in the visualization.
                - `thickness` (int): Thickness of the lines connecting keypoints.
                - `draw_bboxes` (bool): Whether to draw bounding boxes around detected persons.
            Defaults to:
                {
                    "kpt_thr": 0.3,
                    "radius": 5.0,
                    "thickness": 3,
                    "draw_bboxes": False,
                }

    Attributes:
        pose_model: Initialized pose estimation model.
        det_model: Initialized detection model, if provided.
        model_name (str): Name of the pose estimation model class.
        max_people (int): Maximum number of people to detect.
        visualizer: Initialized visualizer object, or `None` if visualization is disabled.
        num_workers (int): Number of worker threads for parallel processing.
        last_detection_duration (float): Duration of the last detection phase in seconds.
        last_pose_estimation_duration (float): Duration of the last pose estimation phase in seconds.
    """

    def __init__(
        self,
        pose_model: str = "RTMPose_Large",
        det_model: Optional[str] = "RTMDetMedium",
        det_thr: float = 0.5,
        max_people: int = -1,
        num_workers: int = 4,
        visualization_config: dict = dict(
            kpt_thr=0.3,
            radius=5.0,
            thickness=3,
            draw_bboxes=False,
        ),
    ):
        # Initialize the pose estimation model
        try:
            self.pose_model = POSE_ESTIMATORS.build(pose_model)
            self.model_name = self.pose_model.__class__.__name__
            logging.info(
                f"Pose estimator '{self.model_name}' initialized successfully."
            )
        except Exception as e:
            logging.error(f"Failed to initialize pose estimator '{pose_model}': {e}")
            raise ValueError(f"Failed to build pose estimator '{pose_model}': {e}")

        # Initialize the detection model if provided
        self.det_model = None
        if det_model:
            try:
                self.det_model = DETECTORS.build(det_model)
                self.det_model.detection_threshold = det_thr
                logging.info(
                    f"Detection model '{det_model}' initialized with threshold {det_thr}."
                )
            except Exception as e:
                logging.error(f"Failed to initialize detector '{det_model}': {e}")
                raise ValueError(f"Failed to build detector '{det_model}': {e}")

        self.max_people = max_people
        logging.debug(f"Maximum number of people to detect set to: {self.max_people}")

        # Initialize the visualizer
        try:
            self.visualizer = VISUALIZERS.build(
                "PoseVisualizer",
                kpts_name=self.pose_model.keypoints_type,
                **visualization_config,
            )
            logging.info("Visualizer initialized successfully.")
        except Exception as e:
            logging.warning(
                f"Failed to initialize visualizer: {e}. Visualization features will be disabled."
            )
            self.visualizer = None

        self.num_workers = num_workers
        logging.debug(f"Number of worker threads set to: {self.num_workers}")

        # Initialize runtime statistics
        self.last_detection_duration = 0.0
        self.last_pose_estimation_duration = 0.0

    @property
    def last_inference_duration(self) -> float:
        """
        Retrieve the total duration of the last inference (detection + pose estimation).

        Returns:
            float: Total inference duration in seconds.
        """
        total_duration = (
            self.last_detection_duration + self.last_pose_estimation_duration
        )
        return total_duration

    def visualize(
        self,
        image: np.ndarray,
        keypoints: List,
        detections: Optional[List] = None,
        return_vis: bool = False,
        save_path: Optional[str] = None,
    ) -> Optional[Image.Image]:
        """
        Generate and handle the visualization of pose estimations on the image.

        Args:
            image (np.ndarray): The original image as a NumPy array.
            keypoints (List): List of detected keypoints for each person.
            detections (Optional[List], optional): List of detection bounding boxes and scores.
                Required if `draw_bboxes` is enabled in visualization config. Defaults to `None`.
            return_vis (bool, optional): If `True`, returns the visualization image.
                If `False`, displays the image. Ignored if `save_path` is provided. Defaults to `False`.
            save_path (Optional[str], optional): File path to save the visualization image.
                If provided, the image will be saved to this path. Defaults to `None`.

        Returns:
            Optional[Image.Image]: The visualization image if `return_vis` is `True` and visualization is enabled;
                otherwise, `None`.
        """
        if self.visualizer is None:
            logging.warning("Visualization is disabled. Skipping visualization step.")
            return None

        try:
            # Generate visualization
            vis_image = self.visualizer.visualize(image, keypoints, detections)
            logging.debug("Visualization created successfully.")
        except Exception as e:
            logging.error(f"Failed to create visualization: {e}")
            return None

        # Handle saving the visualization image
        if save_path:
            try:
                save_dir = os.path.dirname(save_path)
                if save_dir:
                    os.makedirs(save_dir, exist_ok=True)
                    logging.debug(f"Ensured that directory '{save_dir}' exists.")
                vis_image.save(save_path)
                logging.info(f"Visualization image saved to '{save_path}'.")
            except Exception as e:
                logging.error(
                    f"Failed to save visualization image to '{save_path}': {e}"
                )

        # Handle returning or displaying the visualization image
        if return_vis:
            logging.debug("Returning visualization image as requested.")
            return vis_image

        if not save_path:
            try:
                vis_image.show()
                logging.debug("Visualization image displayed successfully.")
            except Exception as e:
                logging.error(f"Failed to display visualization image: {e}")

        return None

    def infer_topdown(self, image: np.ndarray) -> Tuple[List, List]:
        """
        Perform two-stage top-down pose estimation on the given image.

        The process involves detecting persons in the image and then estimating keypoints
        for each detected person in parallel.

        Args:
            image (np.ndarray): The input image as a NumPy array.

        Returns:
            Tuple[List, List]: A tuple containing:
                - List of keypoints for each detected person.
                - List of detection bounding boxes and their confidence scores.
        """
        # Reset runtime statistics
        self.last_detection_duration = 0.0
        self.last_pose_estimation_duration = 0.0

        # Stage 1: Detect persons in the image
        start_time = time.time()
        try:
            detections = self.det_model(image) if self.det_model else []
            logging.info(f"Detected {len(detections)} persons in the image.")
        except Exception as e:
            logging.error(f"Person detection failed: {e}")
            detections = []
        detection_time = time.time() - start_time
        self.last_detection_duration = detection_time
        logging.debug(f"Detection phase took {detection_time:.4f} seconds.")

        if not detections:
            logging.info("No detections found. Skipping pose estimation.")
            return [], []

        # Sort detections by confidence score in descending order
        detections = sorted(detections, key=lambda x: x[1], reverse=True)
        logging.debug("Detections sorted by confidence score.")

        # Limit the number of detections based on `max_people`
        if self.max_people > 0:
            original_count = len(detections)
            detections = detections[: self.max_people]
            logging.info(
                f"Limiting detections from {original_count} to {len(detections)} based on `max_people`."
            )

        # Stage 2: Estimate poses for each detected person in parallel
        keypoints = []
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [
                executor.submit(self.pose_model, image, bbox) for bbox, _ in detections
            ]
            for future in as_completed(futures):
                try:
                    kp = future.result()
                    if kp is not None:
                        keypoints.append(kp)
                        logging.debug("Pose estimated successfully for a detection.")
                    else:
                        logging.warning(
                            "Pose estimation returned None for a detection."
                        )
                except Exception as e:
                    keypoints.append(None)
                    logging.error(f"Pose estimation failed for a detection: {e}")

        pose_estimation_time = time.time() - start_time
        self.last_pose_estimation_duration = pose_estimation_time
        logging.debug(f"Pose estimation phase took {pose_estimation_time:.4f} seconds.")

        return keypoints, detections

    def infer_singlestage(self, image: np.ndarray) -> List:
        """
        Perform single-stage pose estimation on the given image.

        This approach directly estimates keypoints without an intermediate person detection step.
        It is generally not recommended for top-down models as they are optimized for
        working with cropped bounding boxes of detected persons.

        Args:
            image (np.ndarray): The input image as a NumPy array.

        Returns:
            List: List of keypoints estimated for the person in the image.
        """
        # Reset runtime statistics
        self.last_detection_duration = 0.0
        self.last_pose_estimation_duration = 0.0

        # Perform pose estimation
        start_time = time.time()
        try:
            keypoints = self.pose_model(image)
            logging.info("Single-stage pose estimation completed successfully.")
        except Exception as e:
            logging.error(f"Single-stage pose estimation failed: {e}")
            keypoints = []
        pose_estimation_time = time.time() - start_time
        self.last_pose_estimation_duration = pose_estimation_time
        logging.debug(
            f"Single-stage pose estimation took {pose_estimation_time:.4f} seconds."
        )

        return keypoints

    def infer(
        self,
        image_path: str,
        visualize: bool = False,
        return_vis: bool = False,
        save_path: Optional[str] = None,
    ) -> Union[List, Tuple[List, Image.Image]]:
        """
        Perform pose estimation on an image file.

        Depending on the configuration, this method can use a two-stage top-down approach
        (with person detection) or a single-stage approach.

        Args:
            image_path (Union[str, np.ndarray]): Path to the input image file or the image as a numpy array.
            visualize (bool, optional): If `True`, generates and displays a visualization of the poses.
                Overrides `return_vis` and `save_path`. Defaults to `False`.
            return_vis (bool, optional): If `True`, returns the visualization image along with keypoints.
                Ignored if `visualize` is `True` or `save_path` is provided. Defaults to `False`.
            save_path (Optional[str], optional): Directory path to save the visualization image.
                If provided, the image will be saved to this path. Defaults to `None`.

        Returns:
            Union[List, Tuple[List, Image.Image]]: If `return_vis` is `True`, returns a tuple containing
                the list of keypoints and the visualization image. Otherwise, returns only the list
                of keypoints.
        """
        # Load the image
        try:
            if isinstance(image_path, str):
                with Image.open(image_path) as img:
                    image = img.convert("RGB")
                    image_np = np.array(image)
            elif isinstance(image_path, np.ndarray):
                image_np = image_path
            else:
                raise ValueError("Expected image_path to be a str or np.ndarray")
            logging.info(f"Image '{image_path}' loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to open image '{image_path}': {e}")
            raise ValueError(f"Failed to open image '{image_path}': {e}")

        # Perform inference using the appropriate approach
        if self.det_model:
            keypoints, detections = self.infer_topdown(image_np)
        else:
            logging.warning(
                "Single-stage pose estimation is being used. This approach is not recommended for top-down models, "
                "even if only one person is present, as these models are trained to work with cropped bounding boxes. "
                "This may lead to inaccurate results."
            )

            keypoints = self.infer_singlestage(image_np)
            detections = None

        # Handle visualization if requested
        if visualize or return_vis or save_path:
            vis_image = self.visualize(
                image_np,
                keypoints,
                detections,
                return_vis=return_vis,
                save_path=save_path,
            )
            if vis_image is not None and return_vis:
                logging.debug("Returning keypoints and visualization image.")
                return keypoints, vis_image

        logging.info("Pose estimation completed successfully.")
        return keypoints
