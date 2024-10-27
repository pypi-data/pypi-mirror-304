import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np
from PIL import Image, ImageDraw

from pocketpose.registry import DATASETS, VISUALIZERS


@VISUALIZERS.register_module()
class PoseVisualizer:
    def __init__(
        self,
        kpts_name,
        radius: float = 5.0,
        thickness: int = 3,
        kpt_thr: float = 0.3,
        draw_bboxes: bool = False,
    ):
        self.kpts = DATASETS.build(kpts_name)
        self.radius = radius
        self.thickness = thickness
        self.kpt_thr = kpt_thr
        self.draw_bboxes = draw_bboxes
        self.colors = self.generate_colors()
        self.skeleton = self.generate_skeleton()

    def generate_colors(self):
        cmap_name = "hsv"
        num_keypoints = self.kpts.num_keypoints
        cmap = cm.get_cmap(cmap_name)
        color_norm = colors.Normalize(vmin=0, vmax=num_keypoints - 1)
        scalar_map = cm.ScalarMappable(norm=color_norm, cmap=cmap)
        keypoints_colors = [scalar_map.to_rgba(i) for i in range(num_keypoints)]

        # Convert RGBA colors to RGB and scale them to 0-255 integer values
        keypoints_colors = (np.array(keypoints_colors)[:, :3] * 255).astype(np.uint8)

        # convert to list of tuples
        keypoints_colors = [tuple(color) for color in keypoints_colors]
        return keypoints_colors

    def generate_skeleton(self):
        skeleton = []
        edges = self.kpts.edges
        for i, j in edges:
            skeleton.append((i, j, i))
        return skeleton

    def _visualize(self, image, keypoints, bbox=None) -> Image.Image:
        # Draw keypoints
        image_draw = ImageDraw.Draw(image)
        for i, keypoint in enumerate(keypoints):
            x, y, score = keypoint
            if score < self.kpt_thr:
                continue

            if i >= len(self.colors):
                color_index = i % len(self.colors)
            else:
                color_index = i

            # Draw keypoint
            image_draw.ellipse(
                [
                    (x - self.radius, y - self.radius),
                    (x + self.radius, y + self.radius),
                ],
                fill=self.colors[color_index],
            )

        # Draw skeleton
        for i, j, color_index in self.skeleton:
            xi, yi, si = keypoints[i]
            xj, yj, sj = keypoints[j]
            if si > self.kpt_thr and sj > self.kpt_thr:
                image_draw.line(
                    [(xi, yi), (xj, yj)],
                    fill=self.colors[color_index],
                    width=self.thickness,
                )

        # Draw bounding box
        if self.draw_bboxes:
            if bbox is None:
                # Get bounding box coordinates from min/max x/y values
                x_min, y_min = np.min(np.array(keypoints)[:, :2], axis=0)
                x_max, y_max = np.max(np.array(keypoints)[:, :2], axis=0)
                bbox = [(x_min, y_min), (x_max, y_max)]
            else:
                x_min, y_min = bbox[0], bbox[1]
                x_max, y_max = x_min + bbox[2], y_min + bbox[3]

            # Add padding to the bounding box
            padding = self.thickness * 5
            bbox = [
                (x_min - padding, y_min - padding),
                (x_max + padding, y_max + padding),
            ]

            image_draw.rectangle(bbox, outline=(0, 255, 0), width=self.thickness)

        return image

    def _visualize_all(self, image, keypoints, detections=None):
        if detections is not None:
            assert isinstance(detections, list)
            assert isinstance(keypoints, list)
            assert len(detections) == len(keypoints)
            for kpts, (bbox, _) in zip(keypoints, detections):
                image = self._visualize(image, kpts, bbox)
            return image
        else:
            return self._visualize(image, keypoints, None)

    def visualize(self, image, keypoints, detections=None) -> Image.Image:
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        elif isinstance(image, np.ndarray):
            image = Image.fromarray(image).convert("RGB")
        else:
            raise ValueError(
                "Invalid image type. Expected str or np.ndarray, got: ", type(image)
            )

        vis = self._visualize_all(image, keypoints, detections)
        return vis
