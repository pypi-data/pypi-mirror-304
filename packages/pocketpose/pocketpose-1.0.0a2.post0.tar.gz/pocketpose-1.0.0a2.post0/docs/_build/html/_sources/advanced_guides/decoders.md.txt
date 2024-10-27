# Decoders

The decoders are used to convert the raw model output to a keypoint list in the image space. This can include converting heatmaps to keypoint coordinates, or refining the keypoint coordinates using a post-processing algorithm. PocketPose provides a few decoders that can be used out of the box, but you can also create your own decoders. The provided decoders are also used in the models which are bundled with PocketPose.


## Heatmap decoder

The heatmap decoder works by finding the maximum value in each heatmap. The coordinates of the maximum value are then used as the keypoint coordinates, and the value of the maximum is used as the keypoint score. The decoder can be used as follows:

```python
from pocketpose.models.decoder import HeatmapDecoder

decoder = HeatmapDecoder()
keypoints = decoder.decode(heatmaps, image_shape)
```

It expects the heatmaps to be a numpy array of shape `(num_keypoints, heatmap_height, heatmap_width)`, and the image shape to be a tuple of `(image_height, image_width)`. The decoder returns a list of keypoints, where each keypoint is a tuple of `(x, y, score)`. This decoder is used in the `MoveNet` model.

## SimCC decoder

The [SimCC deocder](#) expects the model output to be disentangled horizontal and vertical keypoint coordinates in sub-pixel space. The decoder then uses a post-processing algorithm to refine the keypoint coordinates. The decoder can be used as follows:

```python
from pocketpose.models.decoder import SimCCDecoder

decoder = SimCCDecoder()
keypoints = decoder.decode((simcc_x, simcc_y), image_shape)
```

It expects the model output to be a tuple of `(simcc_x, simcc_y)`, where `simcc_x` and `simcc_y` are numpy arrays of shape `(num_keypoints, heatmap_width * k)` and `(num_keypoints, heatmap_height * k)` respectively. The `k` parameter is the sub-pixel factor, which is the number of sub-pixels per pixel. The image shape should be a tuple of `(image_height, image_width)`. The decoder returns a list of keypoints, where each keypoint is a tuple of `(x, y, score)`. This decoder is used in the `RTMPose` model.

## Refinement decoder

Coming soon...