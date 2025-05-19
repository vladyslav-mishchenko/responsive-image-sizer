"""
main.py

Create images in different sizes for responsive web design breakpoints
Convenient to use with picture html tag
"""

import os
import glob
import json
from PIL import Image
from pathlib import Path
from typing import List, Dict, Any


SOURCES = "sources"
IMAGES = "images"
CONFIGS = "./configs/*.json"


def build_images(source: str, images: str, config: Dict[str, Any]) -> None:
    """
    Read breakpoints configuration
    Create image with width and height
    Save image to destination directory

    Args:
        source (str): source image path
        images (str): destination image path
        config (Dict[str, Any]): image configuration
    """

    path_to_source = os.path.join(source, os.listdir(source)[0])
    path_to_images = Path(images)

    sizes = config["sizes"]
    name = config["name"]
    format = config["format"]

    formates = {
        "webp": {"file_extension": "webp", "pillow_format": "WebP"},
        # "heif": {"file_extension": "heif", "pillow_format": "HEIF"},
        # "avif": {"file_extension": "avif", "pillow_format": "AVIF"},
    }

    image_file_extension = formates[format]["file_extension"]
    pillow_to_save_format = formates[format]["pillow_format"]

    for breakpoint, image_size in sizes.items():
        width = image_size[0]
        # height = image_size[1]
        # size = (width, height)

        image_name = name + "-" + breakpoint + "." + image_file_extension
        path = path_to_images / image_name

        try:
            with Image.open(path_to_source) as image:
                w, h = image.size
                aspect_ratio = h / w

                target_height = int(width * aspect_ratio)
                resized = image.resize((width, target_height), Image.LANCZOS)

                # image.thumbnail(size, Image.LANCZOS)
                resized.save(path, format=pillow_to_save_format, quality=25)

        except Exception as e:
            print(f"Error: {e}")


def read_image_configs(configs: List[Dict[str, Any]]) -> None:
    """
    Read image configs
    Create directories for images id do not exist
    Execure build images function

    Args:
        configs (List[Dict[str, Any]]): list with image config
    """

    for config in configs:
        path_to_images = IMAGES + config["path"]
        path_to_sources = SOURCES + config["path"]

        if os.path.exists(path_to_images):
            build_images(path_to_sources, path_to_images, config)

        else:
            os.makedirs(path_to_images, exist_ok=True)
            build_images(path_to_sources, path_to_images, config)


def read_config_files(files: List[str]) -> None:
    """
    Read list with paths
    Open files by path
    Extract json from files
    Run function that read json config

    Args:
        files (List[str]): list with config files path strings
    """

    for file in files:
        try:
            with open(file, "r") as configs_file:
                image_json_configs = json.load(configs_file)
                read_image_configs(image_json_configs)

        except Exception as e:
            print(f"Error: {e}")


def config_files_list(path: str) -> List[str]:
    """
    Return list with config files paths

    Args:
        path (str): path to config files

    Returns:
        List[str]: paths list
    """

    return glob.glob(path)


def main():
    read_config_files(config_files_list(CONFIGS))


if __name__ == "__main__":
    main()
