<div align="center">
  <img src="resources/logo.svg#gh-light-mode-only" width="100"/>
  <img src="resources/logo-dark.svg#gh-dark-mode-only" width="100"/>
  <div align="center">
        <h1><a href="https://pocketpose.com">PocketPose</a></h1>
    <a href="https://saifkhichi.com">
        Developed by <b>Saif Khan</b>
    </a>
  </div>
  <div>&nbsp;</div>

[![actions](https://github.com/saifkhichi96/pocket-pose/workflows/build/badge.svg)](https://github.com/saifkhichi96/pocket-pose/actions)
[![codecov](https://codecov.io/gh/saifkhichi96/pocket-pose/branch/latest/graph/badge.svg)](https://codecov.io/gh/saifkhichi96/pocket-pose)
[![PyPI](https://img.shields.io/pypi/v/pocket-pose)](https://pypi.org/project/pocket-pose/)
[![LICENSE](https://img.shields.io/github/license/saifkhichi96/pocket-pose.svg)](https://github.com/saifkhichi96/pocket-pose/blob/main/LICENSE)
[![Average time to resolve an issue](https://isitmaintained.com/badge/resolution/saifkhichi96/pocket-pose.svg)](https://github.com/saifkhichi96/pocket-pose/issues)
[![Percentage of issues still open](https://isitmaintained.com/badge/open/saifkhichi96/pocket-pose.svg)](https://github.com/saifkhichi96/pocket-pose/issues)

[📘Documentation](https://pocket-pose.readthedocs.io/latest/) |
[🛠️Installation](https://pocket-pose.readthedocs.io/latest/installation.html) |
[👀Model Zoo](https://pocket-pose.readthedocs.io/latest/model_zoo.html) |
[📜Papers](https://pocket-pose.readthedocs.io/latest/model_zoo_papers/algorithms.html) |
[🆕Update News](https://pocket-pose.readthedocs.io/latest/notes/changelog.html) |
[🤔Reporting Issues](https://github.com/saifkhichi96/pocket-pose/issues/new/choose) |

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

```shell
$ git clone
$ cd pocket-pose
$ pip install .
```

Please refer to the [installation guide](docs/installation.md) for detailed installation instructions.

## Quick Start

Running pose estimation on an image is as simple as:

```python
from pocketpose import PoseInferencer

# Define an input image
image_path = "path/to/image.jpg"  # JPEG or PNG

# Load a model
pose_estimator = PoseEstimator(model_name="model-alias")

# Perform pose estimation
keypoints = pose_estimator.infer(image_path)
```

For more detailed usage and a list of all available models, check out our [usage guide](docs/user_guides/inference.md).

## License
PocketPose is released under the MIT License.
