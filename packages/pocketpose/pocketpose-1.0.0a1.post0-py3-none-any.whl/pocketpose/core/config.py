import json
import os
from typing import Dict

from pocketpose.registry import DATASETS
from pocketpose.utils.io import get_cache_dir


class ModelConfig:
    """Configuration class for a model.

    Attributes:
        name (str): The name of the model.
        pretty_name (str): The printable name of the model.
        input_size (tuple): The input size of the model as (height, width, channels).
        skeleton (str): The skeleton type used by the model.
    """

    SUPPORTED_FORMATS = {
        "tflite": "TFLiteRunner",
        "onnx": "ONNXRunner",
        "task": "MediaPipeRunner",
    }

    class ModelSource:
        """Represents the source of a model.

        Attributes:
            name (str): The name of the source.
            link (str): URL to the original model weights.
            code (str): URL to the original model code.
        """

        def __init__(self, source: Dict) -> None:
            self.name = source.get("name", "Unknown")
            self.link = source.get("link", "")
            self.code = source.get("code", "")

    class DownloadInfo:
        """Represents the download information of a model.

        Attributes:
            float32 (str): URL to download float32 model.
            float16 (str): URL to download float16 model.
            int8 (str): URL to download int8 model.
        """

        SUPPORTED_URLS = ["float32", "float16", "int8"]

        def __init__(self, download: Dict) -> None:
            self.float32 = download.get("float32", None)
            self.float16 = download.get("float16", None)
            self.int8 = download.get("int8", None)

            # At least one download URL must be provided
            if not any([self.float32, self.float16, self.int8]):
                raise ValueError("At least one download URL must be provided.")

            # Set default download URL
            if self.float32:
                self.default = "float32"
            elif self.float16:
                self.default = "float16"
            else:
                self.default = "int8"

        def __getitem__(self, key: str) -> str:
            if key not in self.SUPPORTED_URLS:
                raise ValueError(f'Invalid download key "{key}".')
            return getattr(self, key)

        def __contains__(self, key: str) -> bool:
            return key in self.SUPPORTED_URLS and getattr(self, key) is not None

        def get_default(self) -> str:
            return self[self.default]

    def __init__(self, cfg: Dict):
        self.name = cfg["name"]
        self.pretty_name = cfg.get("pretty_name", self.name)

        # Set input size
        self.input_size = tuple(cfg["input_size"])
        if len(self.input_size) != 3 or self.input_size[2] not in [1, 3]:
            raise ValueError(
                "Input size must be (height, width, channels), and channels must be 1 or 3."
            )

        # Set skeleton type
        self.skeleton = cfg["skeleton"]
        if self.skeleton not in DATASETS:
            raise ValueError(f'Unsupported skeleton type "{self.skeleton}".')

        # Set model format and runner
        self.format = cfg["format"]
        if self.format not in self.SUPPORTED_FORMATS:
            raise ValueError(f'Unsupported model format "{self.format}".')
        self.runner = self.SUPPORTED_FORMATS[self.format]

        # Download and source information
        self.download_info = self.DownloadInfo(cfg["download"])
        self.source_info = self.ModelSource(cfg["source"])

        # Other optional fields
        self.description = cfg.get("description", "")
        self.license = cfg.get("license", "Unknown")
        self.notes = cfg.get("notes", "")
        self.paper = cfg.get("paper", "")

    @property
    def cache_path(self, key: str = None):
        cache_dir = get_cache_dir(subdir="models")
        if key is None:
            key = self.download_info.default
        if key not in self.download_info:
            raise ValueError(f'Download URL for "{key}" not available.')
        filename = f"{self.name}_{key}.{self.format}"
        return os.path.join(cache_dir, filename)

    @property
    def download_path(self, key: str = None):
        if key is None:
            key = self.download_info.default
        if key not in self.download_info:
            raise ValueError(f'Download URL for "{key}" not available.')
        return self.download_info[key]

    def list_available_downloads(self) -> Dict:
        return {key: url for key, url in self.download_info.items() if url}

    def as_dict(self) -> Dict:
        return dict(
            name=self.name,
            pretty_name=self.pretty_name,
            description=self.description,
            notes=self.notes,
            paper=self.paper,
            input_size=self.input_size,
            skeleton=self.skeleton,
            format=self.format,
            runner=self.runner,
            download=self.download_info.default,
            source=self.source_info.name,
            license=self.license,
        )

    @staticmethod
    def fromfile(filename: str, variant: str) -> "ModelConfig":
        with open(filename, "r") as f:
            cfg = json.load(f)
            available_variants = cfg["variants"]
            if variant not in available_variants:
                raise ValueError(f'Model variant "{variant}" not available.')
            return ModelConfig(available_variants[variant])


def load_cfg(path, variant_name):
    return ModelConfig.fromfile(path, variant_name)
