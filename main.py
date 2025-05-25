"""
main.py

Create images in different sizes for responsive web design breakpoints
Convenient to use with picture html tag
"""

import os
import shutil
import glob
import json
from PIL import Image
from pathlib import Path
from typing import List, Dict, Any


SOURCES = "sources"
IMAGES = "images"
CONFIGS = "./configs/**/*.json"


def build_images(config: Dict[str, Any]) -> None:

    images_path = IMAGES + config["images-path"]

    # read breakpoints
    for k, v in config["breakpoints"].items():
        format = "webp"
        image_extention = "webp"
        # format = "AVIF"
        # image_extention = "avif"

        if k == "default":
            format = "JPEG"
            image_extention = "jpg"

        image_name = config["name"] + "-" + k + "." + image_extention
        image = Path(images_path) / image_name

        width = v["width"]
        source = SOURCES + v["source"]
        quality = int(v["quality"])

        try:
            with Image.open(source) as image_source:
                w, h = image_source.size
                aspect_ratio = h / w

                height = int(width * aspect_ratio)
                resized = image_source.resize((width, height), Image.LANCZOS)

                resized.save(image, format=format, quality=quality)
                
                if os.path.exists(image):
                    print(f"image: {image} -> created")

        except Exception as e:
            print(f"{e}")


def create_image_directory(path: str) -> None:
    os.makedirs(path)
    
    if os.path.exists(path):
        print("----------------------------------------------------------------------")
        print(f"directory: {path} -> created")


def read_image_config(config: Dict[str, Any]) -> None:
    path_to_images = IMAGES + config["images-path"]
    create_image_directory(path_to_images)

    build_images(config)


def read_config_files(files: List[str]) -> None:
    """
    Read list with paths
    Open files by path
    Extract json from files
    Run function that read image json config

    Args:
        files (List[str]): list with config files path strings
    """

    for file in files:
        try:
            with open(file, "r") as configs_file:
                image_json_config = json.load(configs_file)
                read_image_config(image_json_config)

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

    return glob.glob(path, recursive=True)


def clear_images_directory() -> None:
    for _ in os.listdir(IMAGES):
        path_to_item = os.path.join(IMAGES, _)

        if os.path.isfile(path_to_item):
            os.remove(path_to_item)

        if os.path.isdir(path_to_item):
            shutil.rmtree(path_to_item)


def main():
    clear_images_directory()
    read_config_files(config_files_list(CONFIGS))
    
    
if __name__ == "__main__":
    main()
