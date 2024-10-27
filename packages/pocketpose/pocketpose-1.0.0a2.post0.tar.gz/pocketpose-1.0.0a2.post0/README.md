<div align="center">
  <img src="resources/logo.svg#gh-light-mode-only" width="100"/>
  <img src="resources/logo-dark.svg#gh-dark-mode-only" width="100"/>
  <div align="center">
        <h1><a href="https://pocketpose.com">PocketPose Python API</a></h1>
    <a href="https://saifkhichi.com">
        Developed by <b>Saif Khan</b>
    </a>
  </div>
  <div>&nbsp;</div>

[![actions](https://github.com/PocketPose/python-api/workflows/build/badge.svg)](https://github.com/PocketPose/python-api/actions)
[![codecov](https://codecov.io/gh/PocketPose/python-api/branch/latest/graph/badge.svg)](https://codecov.io/gh/PocketPose/python-api)
[![PyPI](https://img.shields.io/pypi/v/pocketpose)](https://pypi.org/project/pocketpose/)
[![LICENSE](https://img.shields.io/github/license/PocketPose/python-api.svg)](https://github.com/PocketPose/python-api/blob/main/LICENSE)
[![Average time to resolve an issue](https://isitmaintained.com/badge/resolution/PocketPose/python-api.svg)](https://github.com/PocketPose/python-api/issues)
[![Percentage of issues still open](https://isitmaintained.com/badge/open/PocketPose/python-api.svg)](https://github.com/PocketPose/python-api/issues)

[📘Documentation](https://pocketpose.readthedocs.io/latest/) |
[🛠️Installation](https://pocketpose.readthedocs.io/latest/installation.html) |
[👀Model Zoo](https://pocketpose.readthedocs.io/latest/model_zoo.html) |
[📜Papers](https://pocketpose.readthedocs.io/latest/model_zoo_papers/algorithms.html) |
[🆕Update News](https://pocketpose.readthedocs.io/latest/notes/changelog.html) |
[🤔Reporting Issues](https://github.com/PocketPose/python-api/issues/new/choose) |

</div>

## Introduction

PocketPose is an open-source library that facilitates fast and efficient pose estimation on mobile and edge devices. It supports TensorFlow Lite (TFLite) models and provides a collection of pre-trained models ready to use out of the box.

## Features

- High-performance pose estimation on mobile devices
- Support for TensorFlow Lite models
- Collection of pre-trained models for various use-cases
- Easy-to-use API for custom model deployment

## Installation

PocketPose can be installed from source:

```bash
pip install pocketpose
```

This installs the CPU-only version of PocketPose. To install the GPU version, use:

```bash
pip install pocketpose-gpu
```

Please refer to the [installation guide](docs/installation.md) for detailed installation instructions.

## Quick Start

Running pose estimation on an image is as simple as:

```python
import pocketpose as pp

# Initialize the image inferencer
inferencer = pp.ImageInferencer(
  pose_model="pose-model-alias",
  det_model="detection-model-alias",
  device="cpu",
)

# Estimate keypoints from the image
image_path = "path/to/image.jpg"  # JPEG or PNG
keypoints = inferencer.infer(image_path)

# Visualize and save the keypoints
inferencer.visualize(image_path, keypoints, save_path="path/to/save.jpg")

# Alternatively, visualize directly during inference
# inferencer.infer(image_path, visualize=True, save_path="path/to/save.jpg")

# If save_path is omitted, visualization is displayed on screen
```

For more detailed usage and a list of all available models, check out our [usage guide](docs/user_guides/inference.md).

## License
PocketPose is released under the CC BY-NC 4.0 license. See the [LICENSE](LICENSE) for more details.
