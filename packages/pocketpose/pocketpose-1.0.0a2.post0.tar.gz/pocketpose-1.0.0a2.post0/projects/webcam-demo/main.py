import sys
import time
from typing import Tuple

import cv2
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QBrush, QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QSpinBox,
    QSplashScreen,
    QVBoxLayout,
    QWidget,
)

from pocketpose import ImageInferencer
from pocketpose.apis import list_models
from pocketpose.registry import VISUALIZERS


def resize_with_padding(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
    h, w, c = image.shape
    target_h, target_w = target_size

    # Resize image to fit in target size while maintaining aspect ratio
    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Resize image
    image = cv2.resize(image, (new_w, new_h))

    # Add padding to image
    top = (target_h - new_h) // 2
    bottom = target_h - new_h - top
    left = (target_w - new_w) // 2
    right = target_w - new_w - left

    image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT)

    return image


class CameraView(QLabel):
    def __init__(self, size, flip=True):
        super().__init__()
        self.size = size
        self.flip = flip
        self.resize(*size)
        self.clear()

    def show(self, frame: np.ndarray):
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1) if self.flip else frame
            frame = resize_with_padding(frame, self.size)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(
                frame.data, w, h, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap(convert_to_Qt_format)
            self.setPixmap(pixmap)
        except Exception as e:
            print(e)

    def clear(self):
        # show splash image
        image = cv2.imread("assets/nocamera.jpg")
        image = cv2.flip(image, 1)
        self.show(image)


class Camera:
    def __init__(self, size, camera_id=0):
        self._camera = None
        try:
            self._camera_id = int(camera_id)
        except ValueError:
            self._camera_id = camera_id
        self._is_started = False
        self._view = CameraView(size, flip=isinstance(camera_id, int))

    def start(self):
        if self._is_started:
            return

        if self._camera is None:
            self._view.clear()
            self._camera = cv2.VideoCapture(self._camera_id)

        self._is_started = True

    def pause(self):
        if not self._is_started:
            return

        self._is_started = False

    def read(self):
        if not self._is_started:
            return False, None

        return self._camera.read()

    def release(self):
        if not self._is_started:
            return

        self._camera.release()
        self._camera = None
        self._is_started = False
        self._view.clear()


class WebcamLayout(QVBoxLayout):
    def __init__(self, parent, size, on_frame_fn, refresh_rate=30, camera_id=0):
        super().__init__()
        self.parent = parent
        self.size = size
        self.on_frame_fn = on_frame_fn
        self.refresh_rate = refresh_rate

        # Create the camera
        self.camera = Camera(size, camera_id)
        self.addWidget(self.camera._view)

        # Create the buttons
        self.button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start", parent)
        self.start_button.setStyleSheet("color: black;")
        self.pause_button = QPushButton("Pause", parent)
        self.pause_button.setStyleSheet("color: black;")
        self.stop_button = QPushButton("Stop", parent)
        self.stop_button.setStyleSheet("color: black;")
        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.pause_button)
        self.button_layout.addWidget(self.stop_button)
        self.addLayout(self.button_layout)

        # Create a timer to update the webcam feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(refresh_rate)

        # Connect the buttons to the camera
        self.start_button.clicked.connect(self.on_start)
        self.pause_button.clicked.connect(self.on_pause)
        self.stop_button.clicked.connect(self.on_stop)
        self.on_stop()

    def update(self):
        ret, frame = self.camera.read()
        if not ret or frame is None:
            return

        if self.on_frame_fn is not None:
            frame = self.on_frame_fn(frame)

        self.camera._view.show(frame)

    def on_start(self):
        self.camera.start()
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)

    def on_pause(self):
        self.camera.pause()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def on_stop(self):
        self.camera.release()
        self.start_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.stop_button.setEnabled(False)


class WebcamDemo(QMainWindow):
    def __init__(self, title, size=(800, 600), camera_id=0, default_model=None):
        super().__init__()
        self.setWindowTitle(title)

        # Compute position to center window on screen
        screen = QApplication.desktop().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()
        position = ((screen_width - size[0]) // 2, (screen_height - size[1]) // 2)

        # Set up the main window
        self.setGeometry(*position, *size)
        self.setMaximumHeight(size[1])
        self.setMaximumWidth(size[0])
        self.setFixedSize(*size)
        self.setStyleSheet("color: white;")

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout
        window = QHBoxLayout(central_widget)
        main_column = QVBoxLayout()
        sidebar = QVBoxLayout()
        window.addLayout(sidebar)
        window.addLayout(main_column)

        # Set window background to an image
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setBrush(self.backgroundRole(), QBrush(QPixmap("assets/background.png")))
        self.setPalette(p)

        # Create the webcam view
        camera_width = int(size[0] * 0.5)
        camera_height = int(camera_width / 3 * 4)
        self.webcam_layout = WebcamLayout(
            self, (camera_width, camera_height), self.update_frame, camera_id=camera_id
        )
        main_column.addLayout(self.webcam_layout)

        # Add the pocketpose logo in sidebar with 100x100 size and centered
        logo = QLabel(self)
        logo.setPixmap(
            QPixmap("assets/logo.png").scaled(
                200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        logo.setAlignment(Qt.AlignCenter)
        sidebar.addSpacing(16)
        sidebar.addWidget(logo)
        sidebar.addSpacing(32)

        # Add a round frame inside which the model selector will be placed
        model_selector_frame = QLabel(self)
        model_selector_frame.setPixmap(QPixmap("assets/frame.png").scaled(200, 150))
        sidebar.addWidget(model_selector_frame)
        sidebar.setAlignment(model_selector_frame, Qt.AlignCenter)
        model_selector_frame_layout = QVBoxLayout(model_selector_frame)
        model_selector_frame_layout.setAlignment(model_selector_frame, Qt.AlignCenter)

        # Section heading (centered, bold, larger font, white text)
        model_selector_section_label = QLabel("Inference Parameters", self)
        model_selector_section_label.setStyleSheet(
            "font-weight: bold; font-size: 14px;"
        )
        model_selector_frame_layout.addWidget(model_selector_section_label)

        # Dropdown for model selection
        self.model_selector_label = QLabel("Select a model: ", self)
        model_selector_frame_layout.addWidget(self.model_selector_label)
        self.model_selector = QComboBox(self)
        self.model_selector.setStyleSheet("color: black;")
        self.model_selector.addItems(list_models())
        self.model_selector.currentTextChanged.connect(self.change_model)
        model_selector_frame_layout.addWidget(self.model_selector)

        self.kpt_thr_label = QLabel("Keypoint Threshold: ", self)
        model_selector_frame_layout.addWidget(self.kpt_thr_label)
        self.kpt_thr_slider = QSlider(Qt.Horizontal, self)
        self.kpt_thr_slider.setMinimum(0)
        self.kpt_thr_slider.setMaximum(100)
        self.kpt_thr_slider.setValue(30)
        self.kpt_thr_slider.valueChanged.connect(self.update_visualizer_params)
        model_selector_frame_layout.addWidget(self.kpt_thr_slider)

        # Add 32px of empty space to sidebar to push the model selector and
        # visualizer parameters to the bottom
        sidebar.addSpacing(16)

        # Visualizer parameters
        vizualizer_frame = QLabel(self)
        vizualizer_frame.setPixmap(QPixmap("assets/frame.png").scaled(200, 175))
        sidebar.addWidget(vizualizer_frame)
        sidebar.setAlignment(vizualizer_frame, Qt.AlignCenter)
        vizualizer_frame_layout = QVBoxLayout(vizualizer_frame)
        vizualizer_frame_layout.setAlignment(vizualizer_frame, Qt.AlignCenter)

        # Section heading (centered, bold, larger font, white text)
        vizualizer_section_label = QLabel("Visualizer Parameters", self)
        vizualizer_section_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        vizualizer_frame_layout.addWidget(vizualizer_section_label)

        # Sliders and SpinBoxes for visualization parameters
        self.radius_label = QLabel("Keypoint Radius: ", self)
        vizualizer_frame_layout.addWidget(self.radius_label)
        self.radius_slider = QSlider(Qt.Horizontal, self)
        self.radius_slider.setMinimum(1)
        self.radius_slider.setMaximum(20)
        self.radius_slider.setValue(5)
        self.radius_slider.valueChanged.connect(self.update_visualizer_params)
        vizualizer_frame_layout.addWidget(self.radius_slider)

        self.thickness_label = QLabel("Line Thickness: ", self)
        vizualizer_frame_layout.addWidget(self.thickness_label)
        self.thickness_spinbox = QSlider(Qt.Horizontal, self)
        self.thickness_spinbox.setMinimum(1)
        self.thickness_spinbox.setMaximum(10)
        self.thickness_spinbox.setValue(3)
        self.thickness_spinbox.valueChanged.connect(self.update_visualizer_params)
        vizualizer_frame_layout.addWidget(self.thickness_spinbox)

        self.draw_bbox_checkbox = QCheckBox("Show Bounding Box", self)
        self.draw_bbox_checkbox.stateChanged.connect(self.update_visualizer_params)
        vizualizer_frame_layout.addWidget(self.draw_bbox_checkbox)

        sidebar.addSpacing(16)

        params_frame = QLabel(self)
        params_frame.setPixmap(QPixmap("assets/frame.png").scaled(200, 130))
        sidebar.addWidget(params_frame)
        sidebar.setAlignment(params_frame, Qt.AlignCenter)
        params_frame_layout = QVBoxLayout(params_frame)
        params_frame_layout.setAlignment(params_frame, Qt.AlignCenter)

        params_frame_label = QLabel("Stats", self)
        params_frame_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        params_frame_layout.addWidget(params_frame_label)

        # Labels for stats
        self.fps_label = QLabel("FPS: ", self)
        params_frame_layout.addWidget(self.fps_label)

        self.inference_speed = QLabel("Inference Speed: ", self)
        params_frame_layout.addWidget(self.inference_speed)

        params_frame_layout.addStretch()

        params_frame = QLabel(self)
        params_frame.setPixmap(
            QPixmap("assets/frame.png").scaled(int(0.675 * size[0]), 130)
        )
        main_column.addWidget(params_frame)
        main_column.setAlignment(params_frame, Qt.AlignCenter)
        params_frame_layout = QVBoxLayout(params_frame)
        params_frame_layout.setAlignment(params_frame, Qt.AlignCenter)
        params_frame_layout.addStretch()

        # Add empty space to sidebar to push the model selector and visualizer
        # parameters to the bottom
        sidebar.addStretch()
        main_column.addStretch()

        # Initialize model
        self.available_models = list_models()
        if default_model is None:
            default_model = self.available_models[0]
        self.model_selector.setCurrentText(default_model)
        self.change_model(default_model)

    def change_model(self, model_name):
        self.current_model = model_name
        self.inferencer = ImageInferencer(self.current_model)
        self.visualizer = VISUALIZERS.build(
            "PoseVisualizer", self.inferencer.model.keypoints_type
        )
        self.frame_count = 0
        self.start_time = time.time()
        self.update_visualizer_params()

    def update_visualizer_params(self):
        radius = self.radius_slider.value()
        thickness = self.thickness_spinbox.value()
        kpt_thr = self.kpt_thr_slider.value() / 100.0
        draw_bbox = self.draw_bbox_checkbox.isChecked()
        self.visualizer.radius = radius
        self.visualizer.thickness = thickness
        self.visualizer.kpt_thr = kpt_thr
        self.visualizer.draw_bboxes = draw_bbox

    def update_frame(self, frame):
        # Perform pose inference
        keypoints = self.inferencer.infer(frame)

        # Process frame for display (resize, convert color, draw keypoints)
        frame = self.visualizer.visualize(frame, keypoints)

        # Update frame count and calculate FPS
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            fps = self.frame_count / elapsed_time
            self.fps_label.setText(f"FPS: {fps:.2f}")

        # Update inference speed
        inference_speed = self.inferencer.last_inference_duration_ms
        self.inference_speed.setText(f"Inference Speed: {inference_speed:.2f} ms")

        return frame

    def closeEvent(self, event):
        self.webcam_layout.on_stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", default=0)
    parser.add_argument("--model", type=str, default=None)
    args = parser.parse_args()

    app = QApplication(sys.argv)
    pixmap = QPixmap("assets/splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()

    window = WebcamDemo(
        "PocketPose Webcam Demo", camera_id=args.camera, default_model=args.model
    )
    window.show()
    splash.finish(window)

    sys.exit(app.exec_())
