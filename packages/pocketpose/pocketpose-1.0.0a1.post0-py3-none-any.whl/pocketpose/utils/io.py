import os

import gdown
import numpy as np
import tabulate
import tensorflow as tf
from PIL import Image


def get_cache_dir(subdir: str = None) -> str:
    """Returns the path to the cache directory.

    Args:
        subdir (str): The subdirectory within the cache directory. Defaults to None.

    Returns:
        The path to the cache directory.
    """
    user_dir = os.path.expanduser("~")
    cache_dir = os.path.join(user_dir, ".cache", "pocketpose")
    if subdir is not None:
        cache_dir = os.path.join(cache_dir, subdir)
    return cache_dir


def load_image_from_file(image_path: str, num_channels=3, dtype=np.uint8) -> np.ndarray:
    """Loads an image from a file.

    Args:
        image_path (str): Path to the image file.
        num_channels (int): The number of color channels in the image. Defaults to 3.
        dtype (tf.dtype): The data type of the image. Defaults to tf.uint8 (range [0, 255]).

    Returns:
        The loaded image as a numpy array with shape (height, width, channels).
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB" if num_channels == 3 else "L")
        image = np.array(img, dtype=dtype)
    return image


def resize_image(
    image: np.ndarray,
    size: tuple[int],
    preserve_aspect_ratio=False,
    method="bilinear",
    antialias=True,
) -> np.ndarray:
    """Resizes an image to the specified size.

    Args:
        image (np.ndarray): The image to resize.
        size (tuple[int]): The target size of the image as a tuple (height, width).
        preserve_aspect_ratio (bool): Whether to preserve the aspect ratio of the
                                      image when resizing. If True, the image is padded
                                      with zeros on shorter side to match the target size.
                                      Defaults to False.
        method (str): The interpolation method to use. Must be one of 'nearest',
                        'bilinear' or 'bicubic'. Defaults to 'bilinear'.
        antialias (bool): Whether to use antialiasing when resizing. Defaults to True.

    Returns:
        The resized image as a numpy array with shape (height, width, channels).
    """
    if preserve_aspect_ratio:
        return tf.image.resize_with_pad(
            image, size[0], size[1], method=method, antialias=antialias
        )
    else:
        return tf.image.resize(image, size, method=method, antialias=antialias)


def write_to_table(data, save_path, tablefmt=None):
    """Save the data as a table in the specified format.

    Args:
        data (list of dict): The data to be saved as key-value pairs.
        save_path (str): The path of the file to save the data to.
        tablefmt (str): The format of the table. If None, the format is
                        determined from the extension of the save path.
    """
    # Check the data format
    if not isinstance(data, list) or len(data) == 0 or not isinstance(data[0], dict):
        raise ValueError("The data must be a non-empty list of dictionaries.")

    # Create save directory if it does not exist
    save_dir = os.path.dirname(save_path)
    os.makedirs(save_dir, exist_ok=True)

    ext = os.path.splitext(save_path)[1].lower()
    if tablefmt is None:
        if ext == ".csv":
            tablefmt = "tsv"
        elif ext == ".md":
            tablefmt = "github"
        elif ext == ".rst":
            tablefmt = "rst"
        elif ext == ".html":
            tablefmt = "html"
        elif ext == ".tex":
            tablefmt = "latex"
        else:
            tablefmt = "plain"

    table = tabulate.tabulate(data, headers="keys", tablefmt=tablefmt)
    with open(save_path, "w") as f:
        f.write(table)


def download_file(url, save_path):
    """Download a file from the specified URL.

    Args:
        url (str): The URL to download the file from.
        save_path (str): The path of the file to save the downloaded file to.

    Returns:
        True if the file was downloaded successfully, False otherwise.
    """
    # Create save directory if it does not exist
    save_dir = os.path.dirname(save_path)
    os.makedirs(save_dir, exist_ok=True)

    # Download the file
    try:
        if "drive.google.com" in url and "/view" in url:
            gdown.download(url=url, output=save_path, quiet=False, fuzzy=True)
        else:
            gdown.download(url=url, output=save_path, quiet=False)
        print(f"Saved {save_path}")

    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

    return True
