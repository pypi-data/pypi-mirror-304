# Inference

PocketPose provides the inference interface through the `PoseInferencer` class, which can be used to perform pose estimation on images using any of the pre-trained models available in the library with just a few lines of code.

```python
import pocketpose as pp

image_path = "path/to/image.jpg"  # JPEG or PNG
inferencer = pp.PoseInferencer(model_name="model-alias")
keypoints = inferencer.infer(image_path)
print(keypoints)
```

```text
[(86, 36, 0.49550787), (92, 28, 0.46823704), (81, 31, 0.5882008), (103, 31, 0.49060246), (76, 36, 0.40824494), (119, 67, 0.4409393), (81, 80, 0.6457721), (159, 105, 0.5388895), (54, 116, 0.6067148), (165, 112, 0.14356694), (23, 135, 0.41521636), (148, 168, 0.6924157), (117, 173, 0.5583147), (152, 248, 0.7444087), (86, 225, 0.39080128), (199, 315, 0.5521312), (121, 290, 0.46033904)]
```

This returns a list of keypoints, where each keypoint is a tuple of `(x, y, confidence)` values. To visualize the keypoints on the image, you can use the `return_vis` parameter when creating the `PoseInferencer` object.

```python
inferencer = pp.PoseInferencer(model_name="model-alias", return_vis=True)
keypoints, visualization = inferencer.infer(image_path)
visualization.show()
```

![](_static/images/demos/inference.jpg)

In this case, `visualization` is a `pp.graphics.PoseVisualizer` object which can be used to draw the keypoints on the image. You can also save the visualization to a file or change the appearance of the keypoints using additional parameters in the `PoseInferencer` constructor.

```python
class PoseInferencer:
    """ PoseInferencer provides a unified interface to infer poses from images.

    Args:
        model_name (str): Name of the model to use
        radius (float): Sets the visualization keypoint radius.
        thickness (int): Determines the link thickness for visualization.
        kpt_thr (float): Sets the keypoint score threshold. Keypoints with scores exceeding
                         this threshold will be displayed.
        draw_bbox (bool): Decides whether to display the bounding boxes of instances.
        return_vis (bool): Decides whether to include visualization images in the results.
        vis_out_dir (str): Defines the folder path to save the visualization images. If unset,
                           the visualization images will not be saved.	
    """
    def __init__(self, model_name, radius: float = 5, thickness: int = 3,
                 kpt_thr: float = 0.3, draw_bbox: bool = False, return_vis: bool = False,
                 vis_out_dir: Optional[str] = None):
```
