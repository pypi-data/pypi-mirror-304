import logging
import os
import threading

import cv2

from .stereo_capture import StereoCapture
from .video import VideoCapture

logger = logging.getLogger(__name__)

try:
    import ktb  # https://github.com/nikwl/kinect-toolbox/
    from pylibfreenect2 import Freenect2  # dependency of ktb
except ImportError:
    logger.warning("kinect-toolbox not found, Kinect camera will not work")
    logger.warning(
        "see https://github.com/nikwl/kinect-toolbox/?tab=readme-ov-file#installation"
    )
    ktb = None

from .camera_view import CameraView
from .trackers import SAM2LiveTracker

# Maximum number of cameras supported
# -------------------------------------
# This flag controls how many cameras can be used at the same time. It is arbitrary
# and can be increased if needed. The app looks for up to MAX_CAMERAS cameras and
# makes them available to the user to select from a dropdown menu.
MAX_CAMERAS = 5


def discover_kinects():
    if ktb is None:
        return []

    fn = Freenect2()
    num_devices = fn.enumerateDevices()
    return [f"Kinect {i}" for i in range(num_devices)]


class Camera:
    def __init__(self, size):
        self._camera = None
        self._camera_id = None
        self._is_started = False
        self._is_video = False
        self._view = CameraView(size, flip=True)
        self._tracker = SAM2LiveTracker()
        self.start_frame = 0
        self.end_frame = -1  # -1 means end of video
        self.current_frame = 0
        self.on_camera_changed = lambda: None
        self.on_frame_fn = lambda frame, vis: None

        # Listen to camera view mouse press event
        self._view.mousePressed.connect(self.on_mouse_press)

    def check_camera(self, camera_id):
        if isinstance(camera_id, int) or camera_id.isdigit():
            camera = cv2.VideoCapture(int(camera_id))
            if not camera.isOpened():
                return False
            camera.release()
            return True

        if camera_id == "kinect":
            return ktb is not None

        if isinstance(camera_id, str):
            return os.path.exists(camera_id)

        logger.warning(f"Invalid camera id: {camera_id}")
        return False

    def on_mouse_press(self, x, y, replace=True):
        if replace:
            self._tracker.set_point([x, y])
        else:
            self._tracker.add_point([x, y])
        self._tracker.reset()

    def get_available_cameras(self):
        # Add regular cameras
        cameras = []
        for i in range(MAX_CAMERAS):
            if self.check_camera(i):
                cameras.append(i)

        # Add kinect cameras
        kinects = discover_kinects()
        cameras.extend(kinects)

        return cameras

    def select_default_camera(self):
        cameras = self.get_available_cameras()
        logger.info(f"Available cameras: {cameras}")
        if len(cameras) > 0:
            self.change_camera(cameras[0])
        else:
            raise Exception("No cameras available")

    def change_camera(self, camera_id):
        logger.info(f"Changing camera to {camera_id}")
        self._is_video = False
        self._view.flip = True
        self._tracker.reset()
        if camera_id == "kinect":
            self.release()
            self._camera_id = camera_id
            return

        if isinstance(camera_id, tuple) and len(camera_id) == 2:
            assert isinstance(camera_id[0], int) and isinstance(camera_id[1], int)
            self._camera_id = camera_id
        elif isinstance(camera_id, int) or camera_id.isdigit():
            self._camera_id = int(camera_id)
        else:
            # Must be path to a video file
            if not os.path.exists(camera_id):
                raise Exception("Invalid video file path")
            self._camera_id = camera_id
            self._is_video = True
            self._view.flip = False

        self.release()
        self.start_frame = 0
        self.end_frame = -1
        self.current_frame = 0
        self.on_camera_changed()

    def get_duration(self):
        if not self._is_video:
            return 0

        video = cv2.VideoCapture(self._camera_id)
        fps = video.get(cv2.CAP_PROP_FPS)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        video.release()
        return int(frames / fps)

    def get_fps(self):
        if not self._is_video:
            return 0

        video = cv2.VideoCapture(self._camera_id)
        fps = video.get(cv2.CAP_PROP_FPS)
        video.release()
        return fps

    def set_start_frame(self, start):
        if not self._is_video:
            return

        fps = self.get_fps()
        start_frame = int(start * fps)
        if start_frame != self.start_frame:
            self.start_frame = start_frame
            self.current_frame = start_frame
            # make sure only these frames are read
            self._camera = cv2.VideoCapture(self._camera_id)
            self._camera.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)

            # preview the frame
            ret, frame = self._camera.read()
            self.preview(frame)

            self._camera.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)

    def set_end_frame(self, end):
        if not self._is_video:
            return

        end_frame = int(end * self.get_fps())
        if end_frame != self.end_frame:
            self.end_frame = end_frame

            # preview the frame
            self._camera = cv2.VideoCapture(self._camera_id)
            self._camera.set(cv2.CAP_PROP_POS_FRAMES, self.end_frame)
            ret, frame = self._camera.read()
            self.preview(frame)
            self._camera.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)

    def toggle_start(self):
        if self._is_started:
            self.pause()
        else:
            self.start()

    def screenshot(self):
        import os
        import time

        user_path = os.path.expanduser("~")
        desktop = os.path.join(user_path, "Desktop")
        path = os.path.join(desktop, f"PPStudio_{time.time()}.jpg")
        self._view.pixmap().save(path)
        return path

    def start(self):
        if self._is_started and self._camera is not None:
            return

        if self._camera is None and self._camera_id is not None:
            self._view.clear()
            if isinstance(self._camera_id, str) and self._camera_id.startswith(
                "Kinect"
            ):
                kinect_id = int(self._camera_id.split(" ")[1])
                self._camera = ktb.Kinect(kinect_id)
            elif isinstance(self._camera_id, tuple) and len(self._camera_id) == 2:
                self._is_started = True
                self._camera = StereoCapture(
                    *self._camera_id, sample_rate=24, max_frames=-1
                )
                self._camera.on_frame_captured(self.process_stereo)
                self._is_started = True
                self._camera.start()
            else:
                self._camera = VideoCapture(self._camera_id)
                self._camera.on_frame_captured(self.process)
                self._camera.start()

        self._is_started = True

    def pause(self):
        if not self._is_started or self._camera is None:
            return

        self._is_started = False

    def process_stereo(self, frame1, frame2):
        """
        Processes two video frames by resizing them to the same resolution,
        applying center cropping if their aspect ratios differ, and concatenating them side by side.

        Args:
            frame1 (numpy.ndarray): The first video frame.
            frame2 (numpy.ndarray): The second video frame.
        """

        def center_crop(frame, target_aspect_ratio):
            """
            Crops the input frame to the target aspect ratio centered.

            Args:
                frame (numpy.ndarray): The input image frame.
                target_aspect_ratio (float): The desired aspect ratio (width / height).

            Returns:
                numpy.ndarray: The center-cropped frame.
            """
            height, width = frame.shape[:2]
            current_aspect_ratio = width / height

            if current_aspect_ratio > target_aspect_ratio:
                # Crop width
                new_width = int(height * target_aspect_ratio)
                start_x = (width - new_width) // 2
                cropped_frame = frame[:, start_x : start_x + new_width]
            else:
                # Crop height
                new_height = int(width / target_aspect_ratio)
                start_y = (height - new_height) // 2
                cropped_frame = frame[start_y : start_y + new_height, :]

            return cropped_frame

        # Get original dimensions
        h1, w1 = frame1.shape[:2]
        h2, w2 = frame2.shape[:2]

        # Calculate aspect ratios
        aspect1 = w1 / h1
        aspect2 = w2 / h2

        # Determine the common aspect ratio (use the smaller one to ensure both frames fit)
        common_aspect_ratio = min(aspect1, aspect2)

        # Apply center cropping to both frames to match the common aspect ratio
        frame1_cropped = center_crop(frame1, common_aspect_ratio)
        frame2_cropped = center_crop(frame2, common_aspect_ratio)

        # After cropping, get the new dimensions
        h1_cropped, w1_cropped = frame1_cropped.shape[:2]
        h2_cropped, w2_cropped = frame2_cropped.shape[:2]

        # Determine the target size (use the smallest height and width to maintain consistency)
        target_height = min(h1_cropped, h2_cropped)
        target_width = min(w1_cropped, w2_cropped)

        # Resize both frames to the target size
        frame1_resized = cv2.resize(
            frame1_cropped, (target_width, target_height), interpolation=cv2.INTER_AREA
        )
        frame2_resized = cv2.resize(
            frame2_cropped, (target_width, target_height), interpolation=cv2.INTER_AREA
        )

        # Concatenate the frames horizontally (side by side)
        concatenated_frame = cv2.hconcat([frame1_resized, frame2_resized])

        # Send the concatenated frame for processing
        self.process(True, concatenated_frame)

    def process(self, ret, frame, frame_idx=0):
        # Run this on a worker thread
        threading.Thread(target=self._process, args=(ret, frame, frame_idx)).start()

    def _process(self, ret, frame, frame_idx=0):
        if not self._is_started or self._camera is None:
            return

        if self._camera_id == "kinect":
            color = self._camera.get_frame(ktb.COLOR)
            depth = self._camera.get_frame(ktb.RAW_DEPTH)
            ret, frame, vis = True, (color, depth), None
        else:
            if self._is_video:
                self.current_frame += 1
                if self.end_frame != -1 and self.current_frame > self.end_frame:
                    self.pause()
                    return

        if not ret:
            self.pause()
            return

        # Resize frame to max 640px on the longest side
        max_size = 640
        h, w = frame.shape[:2]
        if h > w:
            small_frame = cv2.resize(frame, (max_size, int(h / w * max_size)))
        else:
            small_frame = cv2.resize(frame, (int(w / h * max_size), max_size))

        if not self._tracker.is_init and self._tracker.can_init():

            def scale(point):
                return [
                    int(point[0] * small_frame.shape[1] / w),
                    int(point[1] * small_frame.shape[0] / h),
                ]

            track_results = self._tracker.init(small_frame, scale_fn=scale)

        else:
            track_results = self._tracker.track(small_frame)

        vis, bbox = self._tracker.visualize(small_frame, track_results)
        vis = cv2.resize(vis, (w, h))

        # scale bbox to original frame size
        if bbox is not None:
            bbox = (
                int(bbox[0] * w / small_frame.shape[1]),
                int(bbox[1] * h / small_frame.shape[0]),
                int(bbox[2] * w / small_frame.shape[1]),
                int(bbox[3] * h / small_frame.shape[0]),
            )

        if not ret or frame is None:
            return

        if self.on_frame_fn is not None:
            frame = self.on_frame_fn(frame, (vis, bbox))

        self.preview(frame)

    def release(self):
        if self._camera is not None:
            if self._camera_id == "kinect":
                self._camera = None
            else:
                self._camera.release()
                self._camera = None

            self._is_started = False
            self._view.clear()

    def preview(self, frame):
        self._view.show(frame)
