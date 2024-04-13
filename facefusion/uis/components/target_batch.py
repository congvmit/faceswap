import os
from glob import glob
from typing import List, Optional, Tuple

import gradio

import facefusion.globals
from facefusion import wording
from facefusion.face_store import clear_reference_faces, clear_static_faces
from facefusion.filesystem import is_image, is_video
from facefusion.uis.core import register_ui_component
from facefusion.uis.typing import File

TARGET_DIR: Optional[gradio.Textbox] = None
TARGET_FILES: Optional[List[gradio.File]] = None
TARGET_DIR_LABEL: Optional[gradio.Label] = None


def render() -> None:
    global TARGET_DIR
    global TARGET_FILES
    global TARGET_DIR_LABEL
    # TARGET_DIR = gradio.File(file_count="directory",
    #                          label="Target Directory",
    #                          file_types=[".png", ".jpg", ".webp"])

    TARGET_DIR = gradio.Textbox(
        label="Target Directory",
        type="text",
        value="/Users/congvm/Workspace/facefusion/inputs",
    )


    TARGET_DIR_LABEL = gradio.Textbox(
        visible=True,
        show_label=False,
        # label="Target Directory Status",
        elem_classes="target_dir_label",
        interactive=False,
    )

    # TARGET_FILES = [
    #     gradio.File(
    #         label="",
    #         file_count="single",
    #         # file_types=[".png", ".jpg", ".webp", ".mp4"],
    #         value=None,
    #         interactive=False,
    #         visible=False,
    #     )
    # ]
    # register_ui_component("target_paths", TARGET_FILES)
    # register_ui_component("target_dir", TARGET_DIR)

def listen() -> None:
    global TARGET_DIR
    global TARGET_FILES
    global TARGET_DIR_LABEL
    TARGET_DIR.change(update_target_paths, inputs=TARGET_DIR, outputs=TARGET_DIR_LABEL)


def update_target_paths(directory: str) -> List[gradio.Label]:
    clear_reference_faces()
    clear_static_faces()

    # Reset target paths
    facefusion.globals.target_paths = []

    if not os.path.isdir(directory):
        return gradio.Textbox(value=f"ERROR: Not a directory {directory} ", visible=True)

    target_paths = glob(directory + "/*.*")

    for target_path in target_paths:
        is_target_image = is_image(target_path)
        is_target_video = is_video(target_path)
        if is_target_image:
            facefusion.globals.target_paths.append(
                {"path": target_path, "type": "image"}
            )
        elif is_target_video:
            facefusion.globals.target_paths.append(
                {"path": target_path, "type": "video"}
            )

    num_videos = len(
        [
            target
            for target in facefusion.globals.target_paths
            if target["type"] == "video"
        ]
    )
    num_images = len(
        [
            target
            for target in facefusion.globals.target_paths
            if target["type"] == "image"
        ]
    )
    return gradio.Textbox(
        value=f"Loaded {len(facefusion.globals.target_paths)} files ({num_videos} Videos + {num_images} Images)",
        visible=True,
    )
