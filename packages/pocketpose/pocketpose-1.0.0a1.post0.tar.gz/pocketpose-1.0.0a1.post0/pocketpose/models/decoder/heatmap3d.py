import numpy as np


class Heatmap3DDecoder:
    def decode(self, prediction, image_shape, depth_scale):
        """
        Decodes a set of 3D heatmaps of shape (K, H, W, D) into (x,y,z) coordinates.

        Parameters:
        - prediction: a numpy array of shape (K, H, W, D) representing the 3D heatmaps for K keypoints.
        - image_shape: a tuple (image_height, image_width) representing the size of the original image.
        - depth_scale: a float representing the scaling factor to convert heatmap depth to real-world depth.

        Returns:
        - keypoints: a list of tuples (x, y, z, score) for each keypoint. x, y are the coordinates in the image space,
          z is the depth in real-world units, and score is the confidence score of the keypoint.
        """
        assert isinstance(prediction, np.ndarray) and len(prediction.shape) == 4
        assert len(image_shape) == 2

        num_keypoints, heatmap_height, heatmap_width, heatmap_depth = prediction.shape
        image_height, image_width = image_shape

        # Scale factors for converting heatmap coordinates to image coordinates
        x_scale = image_width / heatmap_width
        y_scale = image_height / heatmap_height
        z_scale = depth_scale / heatmap_depth

        keypoints = []
        for i in range(num_keypoints):
            # Find the index of the maximum value in the 3D heatmap
            z, y, x = np.unravel_index(
                np.argmax(prediction[i]), (heatmap_depth, heatmap_height, heatmap_width)
            )
            score = prediction[i, z, y, x]

            # Scale the coordinates from heatmap space to image/real-world space
            x = x * x_scale
            y = y * y_scale
            z = z * z_scale

            keypoints.append((int(x), int(y), int(z), score))

        return keypoints
